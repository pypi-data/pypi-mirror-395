# SPDX-License-Identifier: LGPL-2.1-or-later

""" Azure Disk profile representation """

import base64
import json

from cvmutils.guid import EFI_CERT_SHA1_GUID, EFI_CERT_SHA224_GUID, EFI_CERT_SHA256_GUID, EFI_CERT_SHA384_GUID, EFI_CERT_SHA512_GUID
from cvmutils.guid import EFI_CERT_TYPE_X509_GUID, MICROSOFT_GUID

class AZDiskProfile:
    """ Convert Azure disk profile to EFI Signature Lists (ESLs)"""

    def __init__(self, path):
        self.uefi = {}
        with open(path, 'r', encoding="ascii") as f:
            profile = json.loads(f.read())
        for var in ['PK', 'KEK', 'db', 'dbx']:
            self.uefi[var] = base64.b64encode(self.build_esl(profile["properties"]["uefiSettings"]["signatures"][var])).decode('ascii')

    # Each x509 gets its own list as it is unlikely that different x509s have the same size
    def build_esl_x509(self, sigvalues):
        """ Build ESL for x509 """
        res = bytearray()
        for sig in sigvalues:
            sigbytes = base64.b64decode(sig)
            # SignatureType
            res.extend(EFI_CERT_TYPE_X509_GUID.bytes_le)
            # SignatureOwner == 16 bytes + header
            res.extend((len(sigbytes) + 16 + 28).to_bytes(4, 'little'))
            # SignatureHeaderSize
            res.extend((0).to_bytes(4, 'little'))
            # SignatureSize
            res.extend((len(sigbytes) + 16).to_bytes(4, 'little'))
            # MICROSOFT_GUID
            res.extend(MICROSOFT_GUID.bytes_le)
            # Cert
            res.extend(sigbytes)
        return res

    # Sha hashes have the same size and appear as a list
    def build_esl_sha(self, sigvalues, guid):
        """ Build ESL for SHAs """
        res = bytearray()

        if len(sigvalues) == 0:
            return res

        siglen = len(base64.b64decode(sigvalues[0]))
        if guid == EFI_CERT_SHA1_GUID and siglen != 20:
            raise RuntimeError("SHA1 signatures must be 20 bytes long")
        if guid == EFI_CERT_SHA224_GUID and siglen != 28:
            raise RuntimeError("SHA224 signatures must be 28 bytes long")
        if guid == EFI_CERT_SHA256_GUID and siglen != 32:
            raise RuntimeError("SHA256 signatures must be 32 bytes long")
        if guid == EFI_CERT_SHA384_GUID and siglen != 48:
            raise RuntimeError("SHA384 signatures must be 48 bytes long")
        if guid == EFI_CERT_SHA512_GUID and siglen != 64:
            raise RuntimeError("SHA512 signatures must be 64 bytes long")

        # SignatureType
        res.extend(guid.bytes_le)
        # SignatureOwner == 16 bytes to each signature
        res.extend(((siglen + 16) * len(sigvalues) + 28).to_bytes(4, 'little'))
        # SignatureHeaderSize
        res.extend((0).to_bytes(4, 'little'))
        # SignatureSize
        res.extend((siglen + 16).to_bytes(4, 'little'))

        for sig in sigvalues:
            sigbytes = base64.b64decode(sig)
            # MICROSOFT_GUID
            res.extend(MICROSOFT_GUID.bytes_le)
            # Cert
            if len(sigbytes) != siglen:
                raise RuntimeError("All SHA signatures must have the same length")
            res.extend(sigbytes)
        return res

    def build_esl(self, signatures):
        """ Build ESL """

        res = bytearray()
        # PK contains only one signature
        if not isinstance(signatures, list):
            signatures = [signatures]

        for signature in signatures:
            sigtype = signature["type"]
            sigvalues = signature["value"]
            if sigtype == "x509":
                res.extend(self.build_esl_x509(sigvalues))
            elif sigtype == "sha1":
                res.extend(self.build_esl_sha(sigvalues, EFI_CERT_SHA1_GUID))
            elif sigtype == "sha224":
                res.extend(self.build_esl_sha(sigvalues, EFI_CERT_SHA224_GUID))
            elif sigtype == "sha256":
                res.extend(self.build_esl_sha(sigvalues, EFI_CERT_SHA256_GUID))
            elif sigtype == "sha384":
                res.extend(self.build_esl_sha(sigvalues, EFI_CERT_SHA384_GUID))
            elif sigtype == "sha512":
                res.extend(self.build_esl_sha(sigvalues, EFI_CERT_SHA512_GUID))
            else:
                raise RuntimeError(f"Sigtype {sigtype} is unsupported!")
        return res
