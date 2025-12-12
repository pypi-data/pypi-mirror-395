# SPDX-License-Identifier: LGPL-2.1-or-later

""" EFI utils """

import glob
import os
import re
import struct

def get_addons(path: str, ukipath: str) -> list:
    """
    Find all global and UKI specific addons on the ESP
    """
    result = []
    for addonpath in [path + "/loader/addons/", ukipath + ".extra.d/"]:
        if os.path.exists(addonpath):
            for addon in sorted(glob.glob(addonpath + "*.addon.efi")):
                result.append(addon)
    return result

def parse_one_bootline(path: str, vendor: str, bootline: str) -> list:
    """
    Parse one line in BOOTX64.CSV format and return a possible bootchain
    """
    result = []

    # LE mark
    if bootline[0] == '\ufeff':
        bootline = bootline[1:]

    shimpath = f"{path}/EFI/{vendor}/{bootline.split(',')[0].split(' ')[0]}"
    if not os.path.exists(shimpath):
        print(f"Shim {shimpath} from shim fallback doesn't exist!")
        return None

    ukis = []
    ukipath = bootline.split(',')[2].split(' ')[0]
    if ukipath.lower().endswith(".efi"):
        ukipath = re.sub("\\\\", "/", ukipath)
        if not os.path.exists(f"{path}/{ukipath}"):
            print(f"UKI {ukipath} from shim fallback doesn't exist!")
            ukipath = None
        else:
            print(f"Using UKI {ukipath} from shim fallback for PCR prediction")
            ukis.append(f"{path}/{ukipath}")
    else:
        print("BOOTX64.CSV does not set UKI to boot")

    # If UKI is not set in BOOTX64.CSV, shim will attempt to load grubx64.efi
    bootloaderpath = None
    if not ukis:
        bootloaderpath = f"{path}/EFI/{vendor}/grubx64.efi"
        if not os.path.exists(bootloaderpath):
            print("No UKI set in BOOTX64.CSV and grubx64.efi is missing, skipping boot option")
            return None

        ukis = sorted(glob.glob(f"{path}/EFI/Linux/*.efi"))
        if ukis == []:
            print("No UKIs found in /EFI/Linux, skipping boot option")
            return None

        print(f"Using 2nd stage bootloader /EFI/{vendor}/grubx64.efi")

    for ukipath in ukis:
        result.append({"shim": shimpath, "bootloader": bootloaderpath, "uki": ukipath, "addons": get_addons(path, ukipath)})

    return result

def parse_device_path(data: bytes) -> str:
    """
    Parses UEFI Device Path binary to find the File Path string.

    Format:
    [Type (1 byte)] [SubType (1 byte)] [Length (2 bytes)] [Payload...]

    """
    offset = 0

    while offset < len(data):
        # Header is 4 bytes
        if offset + 4 > len(data):
            break

        d_type, d_subtype, d_length = struct.unpack_from('<BBH', data, offset)
        if d_length < 4:
            break

        # Check for Media Device Path (4) -> File Path (4)
        if d_type == 4 and d_subtype == 4:
            # The payload is the file path string (UTF-16LE)
            # Length includes the 4-byte header
            payload_len = d_length - 4
            payload = data[offset+4 : offset+4+payload_len]

            # UEFI strings are null-terminated UTF-16LE
            try:
                # Remove trailing null bytes for cleaner output
                path_str = payload.decode('utf-16-le').rstrip('\x00')
                return path_str
            except UnicodeDecodeError:
                return None

        offset += d_length

    return None

def parse_efivar(efi_data: bytes) -> dict:
    """
    Parse EFIVAR data, format:

    EFI_LOAD_OPTION Header:

    struct {
        UINT32 Attributes;
        UINT16 FilePathListLength;
        CHAR16 Description[];
        EFI_DEVICE_PATH_PROTOCOL FilePathList[];
        UINT8 OptionalData[];
    }
    """

    offset = 0
    if len(efi_data) < 6:
        return None

    # pylint: disable=unused-variable
    load_attributes, path_list_length = struct.unpack_from('<IH', efi_data, offset)
    offset += 6

    # Skip description
    while offset < len(efi_data):
        pair = efi_data[offset:offset+2]
        if len(pair) < 2:
            break

        if pair == b'\x00\x00':
            offset += 2
            break

        offset += 2

    # Extract Device Path List
    if offset + path_list_length > len(efi_data):
        print("Error: Device Path length exceeds file size.")
        return None

    device_path_data = efi_data[offset : offset + path_list_length]
    offset += path_list_length

    # Parse the binary device path to find the string filename
    boot_file = parse_device_path(device_path_data)
    if not boot_file:
        # No file path found, skipping boot option
        return None

    # Extract Optional Data (Boot Options)
    optional_data = efi_data[offset:]

    boot_options_str = ""
    try:
        boot_options_str = optional_data.decode('utf-16-le').rstrip('\x00')
    except UnicodeDecodeError:
        pass

    return {
        "BootFile": boot_file,
        "BootOptions": boot_options_str,
    }

def parse_efivar_file(filepath) -> dict:
    """
    Parse /sys/firmware/efi/efivars/BootXXXX file
    """

    try:
        with open(filepath, 'rb') as f:
            # Read entire file content
            raw_data = f.read()
    except PermissionError:
        print(f"Error: Permission denied reading {filepath}. Try running as root/sudo.")
        return None
    except FileNotFoundError:
        print(f"Error: File {filepath} not found.")
        return None

    # 1. Skip EFIVARFS Attribute Header (4 bytes)
    # The Linux kernel adds a 4-byte attribute header to the file content
    if len(raw_data) < 4:
        print(f"Error: File {filepath} too short to contain kernel attributes.")
        return None

    return parse_efivar(raw_data[4:])

# pylint: disable=too-many-branches
def bootchains_from_shim_fallback(path: str) -> list:
    """
    Discovers possible boot chains from shim fallback file, returns a list of:
    [{"shim": "/path/to/shim", "bootloader": "/path/to/bootloader", "uki": "/path/to/uki", "addons": ["/paths/to/addons"]}]
    """

    result = []

    shimname = 'shim'
    if os.path.exists(f"{path}/EFI/redhat"):
        vendor='redhat'
    elif os.path.exists(f"{path}/EFI/fedora"):
        vendor='fedora'
    elif os.path.exists(f"{path}/EFI/azurelinux"):
        vendor='azurelinux'
    elif os.path.exists(f"{path}/EFI/rocky"):
        vendor='rocky'
    else:
        print("No EFI vendor dir, assuming legacy Mariner 2 layout")
        vendor='BOOT'
        shimname='boot'

    if os.path.exists(f"{path}/EFI/{vendor}/BOOTX64.CSV"):
        fallback = f"{path}/EFI/{vendor}/BOOTX64.CSV"
    elif os.path.exists(f"{path}/EFI/BOOT/BOOTX64.CSV"):
        fallback = f"{path}/EFI/BOOT/BOOTX64.CSV"
    else:
        fallback = None

    if fallback:
        # BOOTX64.CSV may contain several entries
        with open(f"{path}/EFI/{vendor}/BOOTX64.CSV", encoding='utf-16-le') as f:
            for bootline in f.readlines():
                bootchain = parse_one_bootline(path, vendor, bootline)
                if bootchain:
                    result += bootchain
    else:
        # No BOOTX64.CSV, let's hope there's a second stage bootloader
        bootchain = parse_one_bootline(path, vendor, f"{shimname}x64.efi,,,")
        if bootchain:
            result += bootchain

    if result == []:
        raise RuntimeError("No UKI found for PCR prediction!")

    return result

def bootchains_from_efivars(path: str, varspath: str) -> list:
    """
    Discover possible boot chains from efivars directory, returns a list of:
    [{"shim": "/path/to/shim", "bootloader": "/path/to/bootloader", "uki": "/path/to/uki", "addons": ["/paths/to/addons"]}]
    """

    result = []

    for bootfile in sorted(glob.glob(varspath + "/Boot[0-9]*")):
        bootoption = parse_efivar_file(bootfile)
        if not bootoption:
            continue

        shimpath = path + re.sub("\\\\", "/", bootoption['BootFile'])
        if not os.path.isfile(shimpath):
            continue

        ukipath = path + re.sub("\\\\", "/", bootoption['BootOptions'].split(' ')[0])

        if os.path.isfile(ukipath):
            result.append({"shim": shimpath, "bootloader": None, "uki": ukipath, "addons": get_addons(path, ukipath)})
            continue

        # UKI is not [properly] specified -- shim will try loading grubx64.efi
        bootloaderpath = os.path.dirname(shimpath) + "/grubx64.efi"
        if not os.path.exists(bootloaderpath):
            continue

        ukis = sorted(glob.glob(f"{path}/EFI/Linux/*.efi"))
        if ukis == []:
            # No UKIs found in /EFI/Linux, skipping
            continue

        for ukipath in ukis:
            result.append({"shim": shimpath, "bootloader": bootloaderpath, "uki": ukipath, "addons": get_addons(path, ukipath)})

    return result
