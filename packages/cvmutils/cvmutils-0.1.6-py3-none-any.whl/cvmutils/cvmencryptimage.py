# SPDX-License-Identifier: LGPL-2.1-or-later

"""Tool which encrypts OS disk images and seals the key to the target TPM."""

import argparse
import sys
import secrets
import string
import json
import re
import os
import base64
import time
import stat
import ctypes
from cvmutils.efi import bootchains_from_shim_fallback
from cvmutils.pcr import PCR
from cvmutils.sb import SecureBoot
from cvmutils.tools import run_command

LUKSADD_PARAMS = ["-q", "--pbkdf", "pbkdf2", "--pbkdf-force-iterations", "1000"]

# pylint: disable=too-many-locals, too-many-branches, too-many-statements

def is_sha265(value):
    """ Checks whether value is a valid sha256 hash """
    match = re.match(r'^(0x|)\w{64}$', str(value))
    return match is not None

def randpw(length):
    """ Generates a random password of a given length """
    return ''.join([secrets.choice(string.ascii_letters + string.digits) for k in range(length)])

def connect_nbd(args):
    """ Connects image file using qemu-nbd """
    run_command(["modprobe", "nbd"], canfail=True)
    if args.image.endswith(".qcow2"):
        imageformat = "qcow2"
    elif args.image.endswith(".vhd"):
        imageformat = "vpc"
    elif args.image.endswith(".raw"):
        imageformat = "raw"
    else:
        print("Unknown image format, assuming VHD")
        imageformat = "vpc"

    run_command(["qemu-nbd", "-f", imageformat, "-c", f"/dev/nbd{args.nbddev}", args.image], True)
    run_command(["udevadm", "settle"], True)
    time.sleep(1)
    return f"/dev/nbd{args.nbddev}"

def disconnect_nbd(args):
    """ Disconnects image file from qemu-nbd """
    run_command(["qemu-nbd", "-d", f"/dev/nbd{args.nbddev}"])

def connect_image(args):
    """ Connects image file """
    mode = os.stat(args.image).st_mode
    if not stat.S_ISBLK(mode):
        return connect_nbd(args)
    return args.image

def disconnect_image(args):
    """ Disconnects image file """
    mode = os.stat(args.image).st_mode
    if not stat.S_ISBLK(mode):
        disconnect_nbd(args)

def get_partitions(imageblk):
    """ Gets partitions information """
    partitions = {"esp": None, "root": None}
    res = run_command(["lsblk", "-o", "KNAME,PARTTYPE,PARTUUID,UUID", "--json", imageblk])
    lsblk = json.loads(res.stdout)
    for part in lsblk["blockdevices"]:
        if part["parttype"] == "c12a7328-f81f-11d2-ba4b-00a0c93ec93b":
            partitions["esp"] = f"/dev/{part['kname']}"
        elif part["parttype"] == "4f68bce3-e8cd-4db1-96e7-fbcaf984b709":
            partitions["root"] = f"/dev/{part['kname']}"
        elif part["parttype"] == "8da63339-0007-60c0-c436-083ac8230908":
        # 'Linux reserved' partition at 1M offset, used for uefi variables on Azure
            partitions["efivars"] = f"/dev/{part['kname']}"

    if partitions["esp"] is None:
        raise RuntimeError("Image doesn't contain 'EFI System' partition")
    if partitions["root"] is None:
        raise RuntimeError("Image doesn't contain 'Linux root (x86-64)' partition")
    return partitions

def get_partnumber(root_partition):
    """ Gets partition number from name """
    match = re.search(r'\d+$', root_partition)
    if match:
        return match.group(0)
    return None

def encrypt(args):
    """ Encrypt the given image """
    retval = 1
    imageblk = connect_image(args)
    tempdir = None
    try:
        res = run_command(["mktemp", "-d"])
        tempdir = res.stdout[:-1]

        print("Checking image partitions...")
        partitions = get_partitions(imageblk)
        root_pn = get_partnumber(partitions["root"])
        if args.growpart:
            if root_pn:
                print("Trying to grow root partition...")
                run_command(["growpart", "-v", imageblk, root_pn])
            else:
                raise RuntimeError("Failed to find root partition number!")

        res = run_command(["blockdev", "--getsize64", partitions["root"]])
        # 32 mb for LUKS, count in kilobytes
        part2fssz = int(res.stdout) / 1024 - 32 * 1024
        print("Adjusting file system size to accommodate for LUKS metadata...")
        res = run_command(["/sbin/e2fsck", "-f", "-y", partitions["root"]], canfail=True)
        if res.returncode not in [0, 1, 2]:
            raise RuntimeError(f"e2fsck failed with error code {res.returncode}")
        run_command(["resize2fs", partitions["root"], f"{int(part2fssz)}K"])

        lukspw = randpw(32)
        if args.verbose:
            print(f"Cleartext pw is: {lukspw}")

        # Create cloud-init root volume resize key
        if not args.no_cloud_init:
            cloudinitpw = randpw(32)
            if args.verbose:
                print(f"Cloud-init root volume resize key is: {cloudinitpw}")

            with open(tempdir + '/cloudinitpw', 'w', encoding='ascii') as f:
                f.write(cloudinitpw)

            print("Creating cloud-init root volume resize key in /cc_growpart_keydata...")
            cc_clot_id = 1
            run_command(["mkdir", f"{tempdir}/root"])
            run_command(["mount", partitions["root"], f"{tempdir}/root"])
            with open(f"{tempdir}/root/cc_growpart_keydata", 'w', encoding='ascii') as fd:
                keydata = {"key": base64.b64encode(cloudinitpw.encode('ascii')).decode('ascii'),
                           "slot": cc_clot_id}
                if args.verbose:
                    print(f"cloud-init root volume resize /cc_growpart_keydata data: {keydata}")
                fd.write(json.dumps(keydata))
            os.chmod(f"{tempdir}/root/cc_growpart_keydata", stat.S_IRUSR | stat.S_IWUSR)
            run_command(["umount", f"{tempdir}/root"])

        print("Running reencryption...")
        run_command(["cryptsetup", "reencrypt", "--encrypt", "-v", "-q", "--type", "luks2",
                     "--key-file", "-", "--luks2-metadata-size", "512k", "--luks2-keyslots-size",
                     "16384k", "--reduce-device-size", "32768k", partitions["root"]],
                    input=lukspw)
        print("Saving cleartext password as Token 0")
        token0 = {"type": "cleartext", "keyslots": ["0"], "password": lukspw}
        if args.verbose:
            print(f"Token 0: {token0}")
        run_command(["cryptsetup", "token", "import", "--token-id", "0",
                     partitions["root"] ], input=json.dumps(token0))

        # Create cloud init root volume resize keyslot
        if not args.no_cloud_init:
            print("Adding cloud init root volume resize keyslot 1")
            run_command(["cryptsetup", "luksAddKey"] + LUKSADD_PARAMS + ["--key-file", "-",
                        "--key-slot", str(cc_clot_id), partitions["root"], tempdir + '/cloudinitpw'], input=lukspw)

        print("Pre-encryption done!")
        retval = 0
    # pylint: disable=broad-exception-caught
    except Exception as e:
        print(e)
    finally:
        if tempdir:
            run_command(["umount", f"{tempdir}/root"], canfail=True)
            run_command(["rm", "-r", "-f", tempdir], canfail=True)
        disconnect_image(args)
    return retval

def deploy(args):
    """ Seal the key to the given image to the target TPM """
    retval = 1
    tempdir = None
    imageblk = connect_image(args)
    try:
        print("Checking image partitions...")
        partitions = get_partitions(imageblk)
        print("Getting cleartext password...")
        res = run_command(["cryptsetup", "token", "export", "--token-id", "0",
                           partitions["root"] ])
        token0 = json.loads(res.stdout)
        if token0["type"] != "cleartext":
            raise RuntimeError("LUKS token0 doesn't contain cleartext password!")
        lukspw = token0["password"]
        if args.verbose:
            print(f"Cleartext pw is: {lukspw}")

        res = run_command(["mktemp", "-d"])
        tempdir = res.stdout[:-1]

        pcrs_list = []
        pcrs_list_unique = []
        if args.pcr4 == 'auto' or args.pcr7 == 'auto':
            # Mount ESP
            run_command(["mkdir", f"{tempdir}/esp"])
            run_command(["mount", partitions["esp"], f"{tempdir}/esp"])

            sb = SecureBoot(args.nosecureboot)
            if args.efivars_profile:
                sb.load_uefi_from_efivars(args.efivars_profile, args.efivars_profile_no_attrs)
            elif args.uefi_profile:
                sb.load_uefi_from_uefi_profile(args.uefi_profile)
            elif args.az_disk_profile:
                sb.load_uefi_from_azdisk_profile(args.az_disk_profile)
            elif args.pcr7 == 'auto':
                raise RuntimeError("Efivars, UEFI, or Azure disk profile is required for PCR7 prediction")

            for bootchain in bootchains_from_shim_fallback(f"{tempdir}/esp"):
                pcrs = {'bank': 'sha256',
                        'pcrs': []}

                print("Boot chain:", f"shim: {bootchain["shim"].split('/')[-1]}",
                      f"bootloader: {bootchain["bootloader"].split('/')[-1] if bootchain["bootloader"] is not None else ""}",
                      f"uki: {bootchain["uki"].split('/')[-1] if bootchain["uki"] is not None else ""}")
                predictor = PCR(bootchain, sb, args.verbose)

                if args.pcr4:
                    pcrs['pcrs'].append(4)
                    if args.pcr4 != 'auto':
                        pcrs['4'] = args.pcr4
                    else:
                        pcrs['4'] = predictor.predicted_pcr4()
                        print(f"Predicted PCR4 value: {pcrs['4'][2:].lower()}")

                if args.pcr7:
                    pcrs['pcrs'].append(7)
                    if args.pcr7 != 'auto':
                        pcrs['7'] = args.pcr7
                    else:
                        pcrs['7'] = predictor.predicted_pcr7()
                        print(f"Predicted PCR7 value: {pcrs['7'][2:].lower()}")

                pcrs['pcrs'].sort()
                pcrs_list.append(pcrs)

                if args.verbose:
                    print(f"Expected PCR values: {pcrs}")
        else:
            # No prediction is needed, use static values is supplied
            pcrs = {'bank': 'sha256',
                    'pcrs': []}
            if args.pcr4:
                pcrs['pcrs'].append(4)
                pcrs['4'] = args.pcr4
            if args.pcr7:
                pcrs['pcrs'].append(7)
                pcrs['7'] = args.pcr7
            pcrs_list_unique.append(pcrs)

        for pcrs in pcrs_list:
            if not pcrs in pcrs_list_unique:
                pcrs_list_unique.append(pcrs)

        if len(pcrs_list_unique) > 16:
            print("WARNING: too many boot options detected, using the last 16!")
            pcrs_list_unique = pcrs_list_unique[-16:]

        # Check if efivars.json needs to be handled
        if "efivars" in partitions:
            if os.path.exists(f"{tempdir}/esp/efivars.json"):
                with open(partitions["efivars"], "wb") as f:
                    print(f"Writing EFI variables from efivars.json to {partitions['efivars']}")
                    if args.verbose:
                        fstat = os.stat(f"{tempdir}/esp/efivars.json")
                        print(f"efivars.json size is {fstat.st_size}")
                    f.write(ctypes.c_uint32(os.stat(f"{tempdir}/esp/efivars.json").st_size))
                    with open(f"{tempdir}/esp/efivars.json", "rb") as efivars_f:
                        f.write(efivars_f.read())
            else:
                print(f"efivars.json not found in ESP, skipping writing EFI variables to {partitions['efivars']}")
        else:
            if args.verbose:
                print("Can't find a partition to write EFI variables, skipping")

        # Create recovery keyslot
        if args.recovery_key:
            keylength = os.path.getsize(args.recovery_key)
            if keylength == 0:
                raise RuntimeError("Invalid zero-length keyfile")

            if args.recovery_key_type in ['binary', 'both']:
                print(f"Adding recovery keyslot from {args.recovery_key} (binary)")
                run_command(["cryptsetup", "luksAddKey"] + LUKSADD_PARAMS + ["--key-file", "-",
                            partitions["root"], args.recovery_key], input=lukspw)
            if args.recovery_key_type in ['text', 'both']:
                if keylength % 2 != 0:
                    raise RuntimeError(f"Invalid keylength for text keytype: {keylength}")

                print(f"Adding text recovery keyslot from {args.recovery_key} (text)")
                textkey = ""
                with open(args.recovery_key, 'rb') as f:
                    while True:
                        byte2 = f.read(2)
                        if len(byte2) != 2:
                            break
                        textkey += f"{int.from_bytes(byte2, 'little'):05}-"
                textkey=textkey[:-1]
                if args.verbose:
                    print(f"Recovery text key {textkey}")
                with open(tempdir + '/recoverytext', 'w', encoding='ascii') as f:
                    f.write(textkey)
                run_command(["cryptsetup", "luksAddKey"] + LUKSADD_PARAMS + ["--key-file", "-",
                            partitions["root"], tempdir + '/recoverytext'], input=lukspw)

        # Seal the key to the target TPM
        with open(tempdir + '/lukspw', 'w', encoding='ascii') as fd:
            fd.write(lukspw)
        print("Sealing root volume key with systemd-cryptenroll")
        for pcrs in pcrs_list_unique:
            run_command(["systemd-cryptenroll", partitions["root"], "--tpm2-device-key=" + args.srkpub,
                         "--tpm2-pcrs=" + '+'.join(str(key) + ':' + pcrs['bank'] + '=' + pcrs[str(key)] for key in pcrs['pcrs']),
                         "--unlock-key-file=" + tempdir + '/lukspw'])

        # Remove cleartext password
        run_command(["cryptsetup", "token", "remove", "--token-id", "0", partitions["root"]])
        run_command(["cryptsetup", "luksRemoveKey", "--key-file", "-", partitions["root"]], input=lukspw)

        print("Deployment done!")
        retval = 0

    # pylint: disable=broad-exception-caught
    except Exception as e:
        print(e)
    finally:
        if tempdir:
            run_command(["umount", f"{tempdir}/esp"], canfail=True)
            run_command(["rm", "-r", "-f", tempdir], canfail=True)
        disconnect_image(args)
    return retval

def main():
    """ Main runner """
    parser = argparse.ArgumentParser(description='Encrypt/deploy CVM cloud image')
    parser.add_argument('action', choices=['encrypt', 'deploy'], help='encrypt/deploy')
    parser.add_argument('image', help='image file (VHD, QCOW2) or a block device')
    parser.add_argument('-n', '--nbddev', type=int, default=0, help='NBD device number, defaults to 0')
    parser.add_argument('-v', '--verbose', help='Print additional info', action="store_true")
    parser.add_argument('--no-cloud-init', help='Do not create /cc_growpart_keydata and LUKS keyslot for root volume resize (encrypt only)', action="store_true")
    parser.add_argument('-g', '--growpart', help='Grow root partition to the size of the volume (encrypt only)', action="store_true")
    parser.add_argument('-s', '--srkpub', help='SRK public part (\'systemd-analyze srk\', deploy only)')
    parser.add_argument('-u', '--srkunique', help='DEPRECATED')
    parser.add_argument('-r', '--recovery-key', help='Recovery key file (deploy only, adds an additional passphrase to root volume)')
    parser.add_argument('--recovery-key-type', choices=['binary', 'text', 'both'], default='binary', help='Recovery key type')
    parser.add_argument('--noswtpm', help='Do not use swtpm, use hardware /dev/tpm{,rm}0 instead)', action="store_true")
    parser.add_argument('--pcr4',help='Expected PCR4 sha256 value for root volume key sealing (deploy only, sha256 or "auto")')
    parser.add_argument('--pcr7', help='Expected PCR7 sha256 value for root volume key sealing (deploy only, sha256 or "auto")')
    parser.add_argument('--nosecureboot', default=False, help='Do PCR prediction with SecureBoot disabled (deploy only)', action="store_true")
    parser.add_argument('--pcrs-json', help='DEPRECATED')
    profile_group = parser.add_mutually_exclusive_group()
    profile_group.add_argument('--efivars-profile', help='UEFI profile (PK, KEK, db, dbx) efivars-format dir (e.g. /sys/firmware/efi/efivars)) for "--pcr7 auto" (deploy only)')
    profile_group.add_argument('--uefi-profile', help='UEFI profile (PK, KEK, db, dbx) JSON for "--pcr7 auto" (deploy only)')
    profile_group.add_argument('--az-disk-profile', help='Azure disk profile JSON for "--pcr7 auto" (deploy only)')
    parser.add_argument('--efivars-profile-no-attrs', help='The UEFI profile efivars-format files do not include the 4-byte attribute header (--efivars-profile only)', action="store_true")
    parser.add_argument('--seal-type', default='systemd', help='DEPRECATED')
    args = parser.parse_args()

    start = time.time()

    if args.action == 'encrypt':
        retval = encrypt(args)
    else:
        try:
            if not args.srkpub:
                raise RuntimeError("Error: -s/--srkpub argument is mandatory for deployment!")
            if args.pcr4 and args.pcr4 != 'auto' and not is_sha265(args.pcr4):
                raise RuntimeError("Error: PCR4 value must be a valid SHA256 or 'auto'")
            if args.pcr7 and args.pcr7 != 'auto' and not is_sha265(args.pcr7):
                raise RuntimeError("Error: PCR7 value must be a valid SHA256 or 'auto'")
            if args.pcr7 == 'auto' and not any((args.efivars_profile, args.uefi_profile, args.az_disk_profile)):
                raise RuntimeError("Error: '--efivars-profile'/'--uefi-profile'/'--az-disk-profile' must be specified for '--pcr7 auto'")
            if args.pcr7 != 'auto' and any((args.efivars_profile, args.uefi_profile, args.az_disk_profile)):
                raise RuntimeError("Error: '--efivars-profile'/'--uefi-profile'/'--az-disk-profile' can only be used with '--pcr7 auto'")

            if args.seal_type != 'systemd':
                print("WARNING: --seal-type argument is deprecated, only systemd-style sealing is done.")

        # pylint: disable=broad-exception-caught
        except Exception as e:
            print(e, file=sys.stderr)
            sys.exit(1)
        retval = deploy(args)

    end = time.time()

    if retval == 0:
        print(f"{args.action} was successful and took {end-start:.6f} seconds")
    else:
        print(f"{args.action} failed, retval={retval}")

    sys.exit(retval)

if __name__ == '__main__':
    main()
