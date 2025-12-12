# SPDX-License-Identifier: LGPL-2.1-or-later

""" PCR prediction """

import binascii
import hashlib
import struct

from cvmutils.pe import PEImage
from cvmutils.sb import SecureBoot
from cvmutils.guid import GUID_GLOBAL_VARIABLE, GUID_SECURITY_DATABASE, GUID_SHIM_LOCK

# Standard TPM Constants
# Algorithm ID for SHA256 (0x000B)
TPM2_ALG_SHA256 = 0x000B
# Command Code for PolicyPCR (0x0000017F)
TPM_CC_POLICY_PCR = 0x0000017F

def extend_pcr(pcr, digest, verbose, log_prefix):
    """ Extend PCR value (TPM emulation) """
    if verbose:
        print(log_prefix, ''.join(f'{x:02x}' for x in digest))
    return hashlib.sha256(pcr + digest).digest()

def event_hash(guid, name, value):
    """ Event hash (TPM emulation) """
    d = guid.bytes_le
    d += len(name).to_bytes(8, 'little')
    d += len(value).to_bytes(8, 'little')
    d += name.encode('utf-16-le')
    d += value
    return hashlib.sha256(d).digest()

def calculate_pcr_policy(pcr_map: dict) -> str:
    """
    Calculates the PolicyPCR digest for a given set of PCRs and values.

    Note: SHA256 is assumed.
    """

    pcr_value_concat = b''
    # TPM2 PCR selection for 24 PCRs (3 bytes)
    pcr_select_size = 3
    pcr_bitmap = [0] * pcr_select_size

    # PCR bitmap and concatenated PCR values
    for index in sorted(pcr_map.keys()):
        byte_idx = index // 8
        bit_idx = index % 8
        if byte_idx < pcr_select_size:
            pcr_bitmap[byte_idx] |= (1 << bit_idx)
        pcr_value_concat += pcr_map[index]

    pcr_digest = hashlib.sha256(pcr_value_concat).digest()

    # TPML_PCR_SELECTION construction
    tpms_pcr_selection = struct.pack('>HB', TPM2_ALG_SHA256, pcr_select_size)
    tpms_pcr_selection += bytes(pcr_bitmap)
    tpml_pcr_selection = struct.pack('>I', 1) + tpms_pcr_selection

    # NewPolicy = Hash(InitialPolicy || TPM_CC_PolicyPCR || MarshaledSelection || pcrDigest)
    hasher = hashlib.sha256()
    hasher.update(bytearray.fromhex('0000000000000000000000000000000000000000000000000000000000000000'))
    hasher.update(struct.pack('>I', TPM_CC_POLICY_PCR))
    hasher.update(tpml_pcr_selection)
    hasher.update(pcr_digest)

    return hasher.hexdigest()

# pylint: disable=too-many-locals, too-many-branches, too-many-statements, too-many-instance-attributes
class PCR:
    """ PCR4/PCR7 prediction for a given environment """
    def __init__(self, bootchain: dict, sb: SecureBoot, verbose: bool):
        self.verbose = verbose
        self.shim = PEImage(path = bootchain['shim'])
        if bootchain['bootloader'] is not None:
            self.bootloader = PEImage(path = bootchain['bootloader'])
        else:
            self.bootloader = None
        self.uki = PEImage(path = bootchain['uki'])
        self.uki_addons = []
        for addon in bootchain['addons']:
            self.uki_addons.append(PEImage(path = addon))
        self.sb = sb
        self.sb.load_shim(self.shim)
        self.pcr4 = None
        self.pcr7 = None
        self._predict_pcr4()
        self._predict_pcr7()

    def _predict_pcr4(self):
        """ Calculate the expected PCR4 value """

        pcr4 = bytearray.fromhex('0000000000000000000000000000000000000000000000000000000000000000')
        if self.verbose:
            print("PCR4 prediction started: 0000000000000000000000000000000000000000000000000000000000000000")
        # EV_EFI_ACTION
        pcr4 = extend_pcr(pcr4, hashlib.sha256(bytearray(b"Calling EFI Application from Boot Option")).digest(),
                          self.verbose, "PCR4: extending 'Calling EFI Application from Boot Option', hash")
        # EV_SEPARATOR
        pcr4 = extend_pcr(pcr4, hashlib.sha256(bytearray.fromhex("00000000")).digest(),
                          self.verbose, "PCR4: extending '00000000' SEPARATOR, hash")
        # shim
        pcr4 = extend_pcr(pcr4, self.shim.get_authenticode_hash(), self.verbose, "PCR4: extending shim's hash")

        # Second stage bootloader if needed (e.g. sd-boot)
        if self.bootloader is not None:
            pcr4 = extend_pcr(pcr4, self.bootloader.get_authenticode_hash(), self.verbose, "PCR4: extending bootloader's hash")

        # UKI
        pcr4 = extend_pcr(pcr4, self.uki.get_authenticode_hash(), self.verbose, "PCR4: extending UKI's hash")

        # UKI addons
        for addon in self.uki_addons:
            pcr4 = extend_pcr(pcr4, addon.get_authenticode_hash(), self.verbose, f"PCR4: extending UKI's addon {addon.path.split('/')[-1]} hash")

        # With SecureBoot disabled, measure ".linux" section too
        if self.sb.nosecureboot:
            linux = PEImage(data=self.uki.get_section_data(".linux"))
            pcr4 = extend_pcr(pcr4, linux.get_authenticode_hash(), self.verbose, "PCR4: extending Linux's hash")

        self.pcr4 = pcr4

    def _predict_pcr7(self):
        """ Calculate the expected PCR7 value """

        pcr7 = bytearray.fromhex('0000000000000000000000000000000000000000000000000000000000000000')
        if self.verbose:
            print("PCR7 prediction started: 0000000000000000000000000000000000000000000000000000000000000000")

        # SecureBoot state
        if self.sb.nosecureboot:
            expected_sb = '00'
        else:
            expected_sb = '01'

        pcr7 = extend_pcr(pcr7, event_hash(GUID_GLOBAL_VARIABLE, "SecureBoot", bytes.fromhex(expected_sb)),
                          self.verbose, f"PCR7: extending 'SecureBoot: {expected_sb}', hash")

        # PK, KEK, db, dbx
        pcr7 = extend_pcr(pcr7, event_hash(GUID_GLOBAL_VARIABLE, "PK", self.sb.uefi['PK']),
                          self.verbose, "PCR7: extending 'PK' variable, hash")
        pcr7 = extend_pcr(pcr7, event_hash(GUID_GLOBAL_VARIABLE, "KEK", self.sb.uefi['KEK']),
                          self.verbose, "PCR7: extending 'KEK' variable, hash")
        pcr7 = extend_pcr(pcr7, event_hash(GUID_SECURITY_DATABASE, "db", self.sb.uefi['db']),
                          self.verbose, "PCR7: extending 'db' variable, hash")
        pcr7 = extend_pcr(pcr7, event_hash(GUID_SECURITY_DATABASE, "dbx", self.sb.uefi['dbx']),
                          self.verbose, "PCR7: extending 'dbx' variable, hash")

        # EV_SEPARATOR
        pcr7 = extend_pcr(pcr7, hashlib.sha256(bytearray.fromhex("00000000")).digest(),
                          self.verbose, "PCR7: extending '00000000' SEPARATOR, hash")

        # In case several boot components are signed by the same certificate, it is only measured once
        certs_used = []

        if not self.sb.nosecureboot:
            # Certificate which signed shim
            shim_cert_in_db = self.sb.find_shim_cert_in_sb_db()
            if shim_cert_in_db:
                pcr7 = extend_pcr(pcr7, event_hash(GUID_SECURITY_DATABASE, "db", shim_cert_in_db),
                                  self.verbose, "PCR7: shim's signator found in db, extending the matching cert, hash")
                certs_used.append(event_hash(GUID_SECURITY_DATABASE, "db", shim_cert_in_db))
            else:
                raise RuntimeError("SecureBoot certificate which signed Shim can't be found in db!")

        sbat_latest = self.sb.shim_get_sbat_latest()
        if sbat_latest and not self.sb.nosecureboot:
            pcr7 = extend_pcr(pcr7, event_hash(GUID_SHIM_LOCK, "SbatLevel", sbat_latest),
                          self.verbose, "PCR7: extending '.sbatlevel' from shim's binary, hash")
        else:
            # Shim with SecureBoot disabled and older shim versions always
            # measure SBAT_VAR_ORIGINAL (sbat,1,2021030218), fingers crossed
            # it never changes.
            pcr7 = extend_pcr(pcr7, event_hash(GUID_SHIM_LOCK, "SbatLevel", bytearray(b'sbat,1,2021030218\n')),
                              self.verbose, "PCR7: extending '.sbatlevel' 'sbat,1,2021030218', hash")

        if self.sb.shim_measures_moklisttrusted_to_pcr7():
            # MokListTrusted
            pcr7 = extend_pcr(pcr7, event_hash(GUID_SHIM_LOCK, "MokListTrusted", bytes.fromhex('01')),
                              self.verbose, "PCR7: extending 'MokListTrusted: 01', hash")

        # Shim either boots UKI directly or through second state bootloader
        binaries = []
        if not self.sb.nosecureboot:
            if self.bootloader:
                binaries.append((self.bootloader, "bootloader"))
            binaries.append((self.uki, "UKI"))
            for addon in self.uki_addons:
                binaries.append((addon, f"{addon.path.split('/')[1]} addon"))

        for binary, binary_name in binaries:
            found = False
            # Shim measures signators of all valid signatures into PCR7, mimic the behavior.
            for pkcs7 in binary.certchains:
                # Is the certificate which signed the binary in 'db'?
                bin_cert_in_db = self.sb.find_cert_in_sb_db(pkcs7)
                if bin_cert_in_db:
                    found = True
                    ehash = event_hash(GUID_SECURITY_DATABASE, "db", bin_cert_in_db)
                    if ehash not in certs_used:
                        pcr7 = extend_pcr(pcr7, ehash, self.verbose,
                                          f"PCR7: {binary_name}'s signator found in db, extending the matching cert, hash")
                        certs_used.append(ehash)
                    elif self.verbose:
                        print(f"PCR7: {binary_name}'s signator found in db but the hash is already used, skipping")
                    continue

                # Is the certificate which signed the binary is shim's 'vendor_db'?
                vendor_db_cert = self.sb.find_cert_in_shim_vendor_db(pkcs7)
                if vendor_db_cert:
                    found = True
                    ehash = event_hash(GUID_SECURITY_DATABASE, "vendor_db", vendor_db_cert)
                    if ehash not in certs_used:
                        pcr7 = extend_pcr(pcr7, ehash, self.verbose,
                                          f"PCR7: {binary_name}'s signator found in 'vendor_db', extending the matching cert, hash")
                        certs_used.append(ehash)
                    elif self.verbose:
                        print(f"PCR7: {binary_name}'s signator found in 'vendor_db' but the hash is already used, skipping")
                    continue

                # Is the certificate which signed the binary is shim's 'vendor_cert'?
                vendor_cert = self.sb.find_cert_in_shim_vendor_cert(pkcs7)
                if vendor_cert:
                    found = True
                    # shim 15.7+ extends MokListRT and uses it before checking .vendor_cert,
                    # which in practice means that MokListRT entry always gets logged.
                    # See: https://github.com/rhboot/shim/issues/714
                    ehash = event_hash(GUID_SHIM_LOCK, "MokListRT", GUID_SHIM_LOCK.bytes_le + vendor_cert)
                    if ehash not in certs_used:
                        pcr7 = extend_pcr(pcr7, ehash, self.verbose,
                                          f"PCR7: {binary_name}'s signator found in 'vendor_cert', extending the matching cert, hash")
                        certs_used.append(ehash)
                    elif self.verbose:
                        print(f"PCR7: {binary_name}'s signator found in 'vendor_cert' but the hash is already used, skipping")
                    continue

            if not found:
                # Certificate was not found
                raise RuntimeError(f"SecureBoot certificate which signed {binary_name} can't be found in db/shim!")

        self.pcr7 = pcr7

    def predicted_pcr4(self) -> str:
        """ Return predicted PCR4 value """
        return '0x' + binascii.hexlify(self.pcr4).decode('ascii').upper()

    def predicted_pcr7(self) -> str:
        """ Return predicted PCR7 value """
        return '0x' + binascii.hexlify(self.pcr7).decode('ascii').upper()

    def predicted_pcr_policy(self, pcrs: list) -> str:
        """ Predict PCR policy hash """
        pcr_map = {}
        for pcr in sorted(set(pcrs)):
            if pcr == 4:
                pcr_map[4] = self.pcr4
            elif pcr == 7:
                pcr_map[7] = self.pcr7
            else:
                raise RuntimeError(f"PCR{pcr} is not supported!")

        return calculate_pcr_policy(pcr_map)
