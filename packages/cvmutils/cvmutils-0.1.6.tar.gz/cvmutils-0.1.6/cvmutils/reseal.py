# SPDX-License-Identifier: LGPL-2.1-or-later

"""Re-seal volume keys when PCR measurements change."""

import argparse
import json
import os
import re
import sys
from cvmutils.efi import bootchains_from_efivars
from cvmutils.pcr import PCR
from cvmutils.sb import SecureBoot
from cvmutils.tools import run_command

def lsblk_get_crypt_dev(parent: dict) -> list:
    """ Get parent crypt device (partition) from 'lsblk' output """
    ret = []
    if not 'children' in parent or len(parent['children']) == 0:
        return []
    if len(parent['children']) == 1:
        child = parent['children'][0]
        if 'type' in child and child['type'] == 'crypt':
            return [parent['path']]
    for child in parent['children']:
        ret += lsblk_get_crypt_dev(child)
    return ret

def get_crypt_partitions() -> dict:
    """ Get all encrypted partitions which may require re-sealing """
    res = run_command(['lsblk', '--json', '-o', 'NAME,PATH,TYPE'])
    lsblk = json.loads(res.stdout)
    cryptpart = []
    for bd in lsblk['blockdevices']:
        cryptpart += lsblk_get_crypt_dev(bd)
    ret = {}
    for part in cryptpart:
        tokens = {}
        try:
            res = run_command(['cryptsetup', 'luksDump', '--dump-json-metadata', part])
            luksjson = json.loads(res.stdout)
            if not 'tokens' in luksjson:
                continue
            for token_id in luksjson['tokens']:
                token = luksjson['tokens'][token_id]
                if token['type'] != 'systemd-tpm2':
                    continue
                if 'tpm2-pcrs' not in token or token['tpm2-pcrs'] == []:
                    continue
                if 'tpm2-policy-hash' not in token:
                    continue
                tokens[token_id] = token
        # pylint: disable=broad-exception-caught
        except Exception as e:
            print(f'Failed to read tokens for {part}', e)
            continue
        # Skip partitions without 'systemd-tpm2' tokens
        if tokens:
            ret[part] = tokens
    return ret

def get_boot_chains(espmount: str) -> list:
    """ Get possible boot chains """
    if not os.path.isdir(espmount):
        raise RuntimeError('Cannot find EFI partition mount')
    return bootchains_from_efivars(espmount, '/sys/firmware/efi/efivars/')

def print_boot_chain(bootchain: str, espmount: str) -> str:
    """ Pretty print boot chain """
    shimpath = bootchain['shim'].removeprefix(espmount).replace('/', "\\")
    res = f'shim: {shimpath}'
    if bootchain['bootloader']:
        bootloaderpath = bootchain['bootloader'].removeprefix(espmount).replace('/', "\\")
        res += f' bootloader: {bootloaderpath}'
    if bootchain['uki']:
        ukipath = bootchain['uki'].removeprefix(espmount).replace('/', "\\")
        res += f' uki: {ukipath}'
        if bootchain['addons']:
            res += " with addons"
    return res

def cryptenroll_add(partition: str, cryptenroll_pcrs: str, args: argparse.Namespace) -> bool:
    """ Add a keyslot/token with systemd-cryptenroll """
    command = ['systemd-cryptenroll', partition, f'--tpm2-device-key={args.tpm_srk_pub}', f'--tpm2-pcrs={cryptenroll_pcrs}']
    if args.unlock == 'key-file':
        command.append(f'--unlock-key-file={args.unlock_keyfile}')
    elif args.unlock == 'tpm':
        command.append('--unlock-tpm2=auto')
    else:
        raise RuntimeError(f'Unknown LUKS key unlock method {args.unlock}')
    try:
        run_command(command)
        # pylint: disable=broad-exception-caught
    except Exception as e:
        print(e, file=sys.stderr)
        return False
    return True

def cryptenroll_drop(keyslot: str, partition: str) -> bool:
    """ Drop a keyslot/token with systemd-cryptenroll """
    try:
        run_command(['systemd-cryptenroll', f'--wipe-slot={keyslot}', partition])
        # pylint: disable=broad-exception-caught
    except Exception as e:
        print(e, file=sys.stderr)
        return False
    return True

# pylint: disable=too-many-locals, too-many-nested-blocks, too-many-branches, too-many-statements
def reseal(espmount: str, pcrlist: list, args: argparse.Namespace) -> bool:
    """ Re-sealing work """
    result = True
    sb = SecureBoot(False)
    sb.load_uefi_from_efivars('/sys/firmware/efi/efivars/', False)
    partitions = get_crypt_partitions()
    bootchains = get_boot_chains(espmount)
    for partition, parttokens in partitions.items():
        if args.verbose:
            print(f'Checking if partition {partition} requires re-sealing')
        pcrs = []
        pcrs_skipped = []
        if not pcrlist:
            # For '--pcrs auto', check what was previously used
            for token_id, token in parttokens.items():
                if not pcrs:
                    pcrs = token['tpm2-pcrs']
                elif pcrs != token['tpm2-pcrs'] and not token['tpm2-pcrs'] in pcrs_skipped:
                    print(f"Warning: partition {partition} uses various PCR sets, using {pcrs} and skipping {token['tpm2-pcrs']}")
                    pcrs_skipped.append(token['tpm2-pcrs'])
            if args.verbose:
                print(f"Using PCRs {pcrs} for partition {partition}")
        else:
            pcrs = pcrlist
        # Check if we need to issue new tokens
        for bootchain in bootchains:
            if args.verbose:
                print(f'Exploring boot chain: {bootchain}')
            pcr = PCR(bootchain, sb, args.verbose)
            policyhash = pcr.predicted_pcr_policy(pcrs)
            found = False
            for token_id in parttokens:
                token = parttokens[token_id]
                if token['tpm2-pcrs'] != pcrs:
                    continue
                if token['tpm2-policy-hash'] == policyhash:
                    found = True
                    token['reseal-used'] = True
                    if args.verbose:
                        print(f'Partition {partition}: token for pcrs {pcrs} exists')
            if not found:
                print(f'Partition {partition}: need to add new token for pcrs {pcrs} ({print_boot_chain(bootchain, espmount)})')
                pcr_arg = {}
                if 4 in pcrs:
                    pcr_arg[4] = pcr.predicted_pcr4()
                if 7 in pcrs:
                    pcr_arg[7] = pcr.predicted_pcr7()
                cryptenroll_pcrs = '+'.join(str(key) + ':' + 'sha256' + '=' + pcr_arg[key] for key in pcrs)
                print(f'Will{" not" if args.dry_run else "" } add new token for partition {partition} {"(dry-run)" if args.dry_run else ""}')
                if not args.dry_run:
                    result &= cryptenroll_add(partition, cryptenroll_pcrs, args)

        for token_id in parttokens:
            token = parttokens[token_id]
            if not 'reseal-used' in token:
                if args.verbose:
                    print(f'Partition {partition}: token {token_id} for pcrs {token['tpm2-pcrs']} is not used and can be removed')
                if args.remove == 'none':
                    continue
                if args.remove == 'matching' and token['tpm2-pcrs'] != pcrs:
                    continue
                print(f'Will{" not" if args.dry_run else "" } drop unused token {token_id} for partition {partition} {"(dry-run)" if args.dry_run else ""}')
                if not args.dry_run:
                    for keyslot in token['keyslots']:
                        # Let's check that the keyslot is not used somewhere else
                        unused = True
                        for check_token_id in parttokens:
                            check_token = parttokens[check_token_id]
                            if check_token_id != token_id and keyslot in check_token['keyslots']:
                                unused = False
                                print(f'Cannot remove keyslot {keyslot} as it is also used by token {check_token_id}')
                        if unused:
                            result &= cryptenroll_drop(keyslot, partition)
    return result

def main():
    """ Main """
    parser = argparse.ArgumentParser(description='Re-seal volume keys')
    parser.add_argument('-d', '--dry-run', help='List volumes which require re-sealing (dry-run mode)', action='store_true')
    parser.add_argument('-p','--pcrs', help='Comma separated PCRs to use for volume key sealing [4,7], or "auto" (default, means using the existing scheme)', default="auto")
    parser.add_argument('-r', '--remove', choices=['none', 'matching', 'all'],
                        help='Remove unused tokens matching specified PCR set / all', default='none')
    parser.add_argument('-u','--unlock', choices=['tpm', 'key-file'], default='tpm', help='LUKS key unlocking method')
    parser.add_argument('--unlock-keyfile', help='Key file to use for \'key-file\' LUKS key unlocking method')
    parser.add_argument('--tpm-srk-pub', help='TPM SRK public key', default='/run/systemd/tpm2-srk-public-key.tpm2b_public')
    parser.add_argument('-v', '--verbose', help='Print additional info', action='store_true')
    args = parser.parse_args()

    if args.unlock == 'key-file':
        if not args.unlock_keyfile:
            print ('--unlock-keyfile must be specified for "--unlock key-file"')
            sys.exit(1)
        if not os.path.isfile(args.unlock_keyfile):
            print (f'{args.unlock_keyfile} file does not exist or is not a regular file')
            sys.exit(1)

    if not os.path.isfile(args.tpm_srk_pub):
        print (f'{args.tpm_srk_pub} file does not exist or is not a regular file')
        sys.exit(1)

    if args.pcrs == "auto":
        pcrs = []
    else:
        # Support "--pcrs 4+7, --pcrs 4,7"
        pcrs = set()
        for pcr in re.split(r'[,+ ]+', args.pcrs):
            if pcr == '4':
                pcrs.add(4)
            elif pcr == '7':
                pcrs.add(7)
            else:
                print('Only PCRs 4 and 7 are currently supported')
                sys.exit(1)
        pcrs = list(pcrs)

    res = run_command(['bootctl', '-p'])
    espmount = res.stdout.split('\n')[0]

    if not reseal(espmount, pcrs, args):
        sys.exit(1)

if __name__ == '__main__':
    main()
