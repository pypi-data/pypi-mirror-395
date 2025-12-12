# SPDX-License-Identifier: LGPL-2.1-or-later

""" Parse PE binaries. Borrowed from https://gitlab.com/berrange/tpm-prevision/ """

import hashlib
import io

# pylint: disable=too-many-locals, too-many-branches, too-many-statements

class PEImage:
    """ PE binary
    Format:
      https://learn.microsoft.com/en-us/windows/win32/debug/pe-format
      https://upload.wikimedia.org/wikipedia/commons/1/1b/Portable_Executable_32_bit_Structure_in_SVG_fixed.svg
    """

    # Magic bytes 'MZ'
    DOS_SIG = bytes([0x4d, 0x5a])

    # Offset in DOS header where the PE offset live
    DOS_HEADER_FIELD_PE_OFFSET = 0x3c

    # Magic bytes 'PE\0\0'
    PE_SIG = bytes([0x50, 0x45, 0x00, 0x00])

    # Offsets relative to start of PE_SIG
    PE_HEADER_FIELD_MACHINE = 0x4
    PE_HEADER_FIELD_NUMBER_OF_SECTIONS = 0x6
    PE_HEADER_FIELD_POINTER_TO_SYMBOL_TABLE = 0xc
    PE_HEADER_FIELD_NUMBER_OF_SYMBOLS = 0x10
    PE_HEADER_FIELD_SIZE_OF_OPTIONAL_HEADER = 0x14
    PE_HEADER_SIZE = 0x18

    MACHINE_I686 = 0x014c
    MACHINE_X86_64 = 0x8664
    MACHINE_AARCH64 = 0xaa64

    MACHINES = [MACHINE_I686,
                MACHINE_X86_64,
                MACHINE_AARCH64]


    PE32_SIG = bytes([0x0b, 0x01])
    PE32P_SIG = bytes([0x0b, 0x02])

    # Offsets relative to PE_HEADER_SIZE
    PE32X_HEADER_FIELD_SIZE_OF_HEADERS = 0x3c
    PE32X_HEADER_FIELD_CHECKSUM = 0x40
    PE32_HEADER_FIELD_CERT_TABLE = 0x80
    PE32P_HEADER_FIELD_CERT_TABLE = 0x90

    SECTION_HEADER_FIELD_VIRTUAL_SIZE = 0x8
    SECTION_HEADER_FIELD_SIZE = 0x10
    SECTION_HEADER_FIELD_OFFSET = 0x14
    SECTION_HEADER_LENGTH = 0x28

    def __init__(self, path=None, data=None):
        self.path = path
        self.data = data
        self.sections = {}
        self.authenticodehash = None
        self.certchains = []
        self.load()

    def has_section(self, name):
        """ Checks if binary has a certain section """
        return name in self.sections

    def get_section_data(self, name):
        """ Get section """
        if name not in self.sections:
            raise RuntimeError(f"Missing section '{name}'")

        start, end = self.sections[name]
        with open(self.path, 'rb') as fp:
            fp.seek(start)
            return fp.read(end-start)

    def get_authenticode_hash(self):
        """ Get Authenticode hash """
        return self.authenticodehash

    def load(self):
        """ Load PE binary """
        if self.path is not None:
            with open(self.path, 'rb') as fp:
                self.load_fh(fp)
        elif self.data is not None:
            with io.BytesIO(self.data) as fp:
                self.load_fh(fp)
        else:
            raise RuntimeError("Either path or data is required")

    def load_fh(self, fp):
        """ Load PE binary from a file """
        dossig = fp.read(2)
        if dossig != self.DOS_SIG:
            raise RuntimeError(f"Missing DOS header magic {self.DOS_SIG} got {dossig}")

        fp.seek(self.DOS_HEADER_FIELD_PE_OFFSET)
        peoffset = int.from_bytes(fp.read(4), 'little')
        fp.seek(peoffset)

        pesig = fp.read(4)
        if pesig != self.PE_SIG:
            raise RuntimeError(f"Missing PE header magic {self.PE_SIG} at {peoffset:x} got {pesig}")

        fp.seek(peoffset + self.PE_HEADER_FIELD_MACHINE)
        pemachine = int.from_bytes(fp.read(2), 'little')

        if pemachine not in self.MACHINES:
            raise RuntimeError(f"Unexpected PE machine architecture 0x{pemachine:x} expected {', '.join([f'0x{m:x}' for m in self.MACHINES])}")

        fp.seek(peoffset + self.PE_HEADER_FIELD_NUMBER_OF_SECTIONS)
        num_of_sections = int.from_bytes(fp.read(2), 'little')

        fp.seek(peoffset + self.PE_HEADER_FIELD_SIZE_OF_OPTIONAL_HEADER)
        size_of_optional_header = int.from_bytes(fp.read(2), 'little')

        fp.seek(peoffset + self.PE_HEADER_FIELD_POINTER_TO_SYMBOL_TABLE)
        pointer_to_symbol_table = int.from_bytes(fp.read(4), 'little')

        fp.seek(peoffset + self.PE_HEADER_FIELD_NUMBER_OF_SYMBOLS)
        number_of_symbols = int.from_bytes(fp.read(4), 'little')

        # image loader header follows PE header
        fp.seek(peoffset + self.PE_HEADER_SIZE)

        ldrsig = fp.read(2)
        if pemachine == self.MACHINE_I686:
            wantldrsig = self.PE32_SIG
            certtableoffset = self.PE32_HEADER_FIELD_CERT_TABLE
        else:
            wantldrsig = self.PE32P_SIG
            certtableoffset = self.PE32P_HEADER_FIELD_CERT_TABLE

        if ldrsig != wantldrsig:
            raise RuntimeError(f"Missing image loader signature {wantldrsig.hex()} got {ldrsig.hex()}")

        # Extract all PKCS7 objects from cert table
        certchains = []

        fp.seek(peoffset + self.PE_HEADER_SIZE + self.PE32X_HEADER_FIELD_SIZE_OF_HEADERS)
        size_of_headers = int.from_bytes(fp.read(4), 'little')

        fp.seek(peoffset + self.PE_HEADER_SIZE + certtableoffset)
        cert_table_offset = int.from_bytes(fp.read(4), 'little')

        fp.seek(peoffset + self.PE_HEADER_SIZE + certtableoffset + 4)
        cert_table_size = int.from_bytes(fp.read(4), 'little')

        offset = 0
        while offset < cert_table_size:
            fp.seek(cert_table_offset + offset)
            certlen = int.from_bytes(fp.read(4), 'little')
            certrev = int.from_bytes(fp.read(2), 'little')
            certtype = int.from_bytes(fp.read(2), 'little')
            if certtype == 2 and certrev == 0x200 and certlen:
                pkcs7 = fp.read(certlen - 8)
                certchains.append(pkcs7)
            offset += ((offset + certlen + 7) // 8) * 8

        # When hashing the file, we need to exclude certain areas
        # with variable data as detailed in:
        #
        # https://reversea.me/index.php/authenticode-i-understanding-windows-authenticode/
        #
        # so build a list of start/end offsets to hash over
        tohash = [
            # From start of file, to the checksum
            [0, peoffset + self.PE_HEADER_SIZE + self.PE32X_HEADER_FIELD_CHECKSUM],

            # From after checksum, to the certificate table
            [peoffset + self.PE_HEADER_SIZE + self.PE32X_HEADER_FIELD_CHECKSUM + 4,
             peoffset + self.PE_HEADER_SIZE + certtableoffset],

            # From after certificate table to end of headers
            [peoffset + self.PE_HEADER_SIZE + certtableoffset + 8,
             size_of_headers],
        ]

        image_data_length = size_of_headers
        next_section = peoffset + self.PE_HEADER_SIZE + size_of_optional_header
        for _ in range(num_of_sections):
            fp.seek(next_section)
            name = fp.read(8).decode('ascii').rstrip('\0')

            if len(name) and name[0] == '/':
                # This is a long name, must check strings table. String table is located
                # right after symbols table, every entry in symbols table is 18 bytes long.
                string_offset = pointer_to_symbol_table + (number_of_symbols * 18)
                string_offset += int(name[1:])
                fp.seek(string_offset)
                name = ""
                while True:
                    b = fp.read(1)
                    if len(b) and b != b'\x00':
                        name += b.decode('ascii')
                    else:
                        break

            fp.seek(next_section + self.SECTION_HEADER_FIELD_OFFSET)
            section_offset = int.from_bytes(fp.read(4), 'little')
            fp.seek(next_section + self.SECTION_HEADER_FIELD_SIZE)
            section_size = int.from_bytes(fp.read(4), 'little')
            fp.seek(next_section + self.SECTION_HEADER_FIELD_VIRTUAL_SIZE)
            section_virtual_size = int.from_bytes(fp.read(4), 'little')

            if section_size != 0:
                tohash.append([section_offset, section_offset + section_size])
                image_data_length += section_size
                self.sections[name] = [section_offset, section_offset + section_virtual_size]
            next_section += self.SECTION_HEADER_LENGTH


        file_length = fp.seek(0, 2) - cert_table_size

        if image_data_length < file_length:
            tohash.append([image_data_length, file_length])

        tohash = sorted(tohash, key=lambda r: r[0])

        h = hashlib.new('sha256')
        for area in tohash:
            fp.seek(area[0])
            h.update(fp.read(area[1]-area[0]))

        self.certchains = certchains
        self.authenticodehash = h.digest()
