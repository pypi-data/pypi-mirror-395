# SPDX-License-Identifier: LGPL-2.1-or-later

""" SecureBoot configuration representation """

import base64
import json
import re
import io

from cvmutils.guid import GUID_GLOBAL_VARIABLE, GUID_SECURITY_DATABASE, EFI_CERT_TYPE_X509_GUID
from cvmutils.tools import run_command
from cvmutils.azdisk import AZDiskProfile

class SecureBoot:
    """ SecureBoot configuration """

    def __init__(self, nosecureboot: bool):
        self.uefi = {}
        self.db_x509_certs = []
        self.shim = None
        self.shim_vendor_cert = []
        self.shim_vendor_db = []
        self.nosecureboot = nosecureboot

    def load_uefi_from_efivars(self, path, no_attrs):
        """ Load configuration from Efivars """

        for var, guid in [('PK', GUID_GLOBAL_VARIABLE), ('KEK', GUID_GLOBAL_VARIABLE), ('db', GUID_SECURITY_DATABASE), ('dbx', GUID_SECURITY_DATABASE)]:
            filename = f'{path}/{var}-{guid}'
            try:
                with open(filename, 'br') as f:
                    data = f.read()
            except Exception as exc:
                raise RuntimeError(f'Could not read efivars file: {filename}') from exc
            if not no_attrs:
                # efivars files from efivarfs contain a 4-byte header with the var attrs that we need to skip over
                data = data[4:]
            self.uefi[var] = data
        self.db_x509_certs = self.__get_db_certs(self.uefi['db'])

        # Optionally, check if SecureBoot is enabled
        try:
            with open(f'{path}/SecureBoot-{GUID_GLOBAL_VARIABLE}', 'br') as f:
                data = f.read()
        except (IOError, FileNotFoundError):
            pass
        if not no_attrs:
            # skip 4-byte header
            data = data[4:]
        if data == b'\x01':
            self.nosecureboot = False
        elif data == b'\x00':
            self.nosecureboot = False
        else:
            print("Unsupported SecureBoot efivar format")

    def load_uefi_from_uefi_profile(self, path):
        """ Load configuration from UEFI profile """

        with open(path, 'r', encoding='ascii') as f:
            json_uefi = json.loads(f.read())
        for var in 'PK', 'KEK', 'db', 'dbx':
            self.uefi[var] = base64.b64decode(json_uefi[var])
        self.db_x509_certs = self.__get_db_certs(self.uefi['db'])

    def load_uefi_from_azdisk_profile(self, path):
        """ Load configuration from Azure Disk profile """

        profile = AZDiskProfile(path)
        for var in 'PK', 'KEK', 'db', 'dbx':
            self.uefi[var] = base64.b64decode(profile.uefi[var])
        self.db_x509_certs = self.__get_db_certs(self.uefi['db'])

    def __get_db_certs(self, db):
        """ Get all certs in 'db' """

        certs = []
        offset = 0

        while offset < len(db) - 28:
            list_type = db[offset:offset + 16]
            list_size = int.from_bytes(db[offset + 16:offset + 20], 'little')
            head_size = int.from_bytes(db[offset + 20:offset + 24], 'little')
            item_size = int.from_bytes(db[offset + 24:offset + 28], 'little')

            if offset + list_size > len(db):
                raise RuntimeError("Invalid list size!")

            offset += (28 + head_size)
            item_offset = 0

            if list_type == EFI_CERT_TYPE_X509_GUID.bytes_le:
                while item_offset < list_size - (head_size + 28):
                    item = db[offset + item_offset:offset + item_offset + item_size]
                    res = run_command(["openssl", "x509", "-inform", "der", "-subject", "-issuer"], input=item[16:], text=False)

                    for subject, issuer in re.findall("^subject=(.*)\n^issuer=(.*)", res.stdout.decode('ascii'), re.MULTILINE):
                        certs.append({"subject": subject, "issuer": issuer, "bytes": item})

                    item_offset += item_size

            offset += list_size - (28 + head_size)

        return certs

    def __find_cert_in_db(self, pkcs7, db):
        """ Find matching cert in 'db' """

        certs_list = []

        res = run_command(["openssl", "pkcs7", "-inform", "der", "-print_certs"], input=pkcs7, text=False)
        certs_list.extend(re.findall("^subject=(.*)(?:\n)+^issuer=(.*)\n", res.stdout.decode('ascii'), re.MULTILINE))

        for subject_bin, issuer_bin in certs_list:
            # Compare CNs only!
            for x509_cert in db:
                # The same or parent
                if x509_cert['subject'] in [subject_bin, issuer_bin]:
                    return x509_cert['bytes']
        return None

    def find_cert_in_sb_db(self, pkcs7):
        """ Find cert in SecureBoot 'db' """

        return self.__find_cert_in_db(pkcs7, self.db_x509_certs)

    def load_shim(self, shim):
        """ Load shim binary """

        self.shim = shim

        if not self.shim.has_section(".vendor_cert"):
            return

        data = io.BytesIO(self.shim.get_section_data(".vendor_cert"))
        try:
            auth_size = int.from_bytes(data.read(4), 'little')
            # pylint: disable=unused-variable
            deauth_size = int.from_bytes(data.read(4), 'little')
            auth_off_t = int.from_bytes(data.read(4), 'little')
            # pylint: disable=unused-variable
            deauth_off_t = int.from_bytes(data.read(4), 'little')

            data.seek(auth_off_t)

            vc = data.read(auth_size)

            # Is this an x509 cert ('vendor_cert' format)?
            res = run_command(["openssl", "x509", "-inform", "der", "-subject", "-issuer"], input=vc, text=False, canfail=True)
            if res.returncode == 0:
                for subject, issuer in re.findall("^subject=(.*)\n^issuer=(.*)", res.stdout.decode('ascii'), re.MULTILINE):
                    self.shim_vendor_cert.append({"subject": subject, "issuer": issuer, "bytes": vc})
                return

            # The other option is 'vendor_db' format
            self.shim_vendor_db = self.__get_db_certs(vc)

        # pylint: disable=broad-exception-caught
        except Exception:
            print("Unsupported shim .vendor_cert section format: %")

    def find_shim_cert_in_sb_db(self):
        """ Find shim signing cert in SecureBoot 'db' """

        for pkcs7 in self.shim.certchains:
            cert = self.__find_cert_in_db(pkcs7, self.db_x509_certs)
            # OVMF stops when it find the first valid signature and only measures
            # that in PCR7
            if cert:
                return cert
        return None

    def find_cert_in_shim_vendor_cert(self, pkcs7):
        """ Find cert in shim 'vendor_cert' """

        return self.__find_cert_in_db(pkcs7, self.shim_vendor_cert)

    def find_cert_in_shim_vendor_db(self, pkcs7):
        """ Find cert in shim 'vendor_db' """

        return self.__find_cert_in_db(pkcs7, self.shim_vendor_db)

    def shim_measures_moklisttrusted_to_pcr7(self):
        """
        Check if shim measures 'MokListTrusted' to PCR7.

        Shim before 15.7 was wrongly measuring "MokListTrusted: 01" into PCR7, see
        https://github.com/rhboot/shim/issues/484
        Use shim's .sbat section to detect older version. Note, nothing older that
        15.5 was ever supported by this tool so just try our best to detect 15.5 and
        15.6.
        """
        if not self.shim.has_section(".sbat"):
            return False
        try:
            sbat = self.shim.get_section_data(".sbat").decode('ascii').split('\n')
            for sbat_line in sbat:
                entries = sbat_line.split(',')
                if len(entries) < 5:
                    continue
                if entries[0].strip() == 'shim.redhat' and entries[4].strip() in ['15.5', '15.6']:
                    return True
        # pylint: disable=broad-exception-caught
        except Exception:
            pass

        return False

    def shim_get_sbat_latest(self):
        """ Get the latest SBAT level """

        if not self.shim.has_section(".sbatlevel"):
            return None

        sbat_section = io.BytesIO(self.shim.get_section_data(".sbatlevel"))

        magic = int.from_bytes(sbat_section.read(4), 'little')
        if magic != 0:
            return None

        off_t_prev = int.from_bytes(sbat_section.read(4), 'little')
        # pylint: disable=unused-variable
        off_t_latest = int.from_bytes(sbat_section.read(4), 'little')

        # account for magic
        sbat_section.seek(off_t_prev + 4)

        # 'latest' is the last section, read untill the end
        sbat_bytes = sbat_section.read()

        # string must be null terminated
        if sbat_bytes.find(0) != -1:
            return sbat_bytes[0:sbat_bytes.find(0)]

        return None
