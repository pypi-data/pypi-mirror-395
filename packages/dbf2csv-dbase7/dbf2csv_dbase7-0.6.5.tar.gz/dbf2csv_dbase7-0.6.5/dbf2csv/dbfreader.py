import csv
import datetime
import decimal
import struct
from pathlib import Path
from typing import Union

from .dbfsignature import dbf_version

# Versiones implementadas
_IMPLEMENTED = {0x04}  # dBASE 7


def b2str(b: bytes, encoding="utf8") -> str:
    return b.replace(b"\0", b"").decode(encoding=encoding)


def dbf2csv(dbf_file, csv_file):
    DBFile(Path(dbf_file).read_bytes()).to_csv(csv_file)


class DBFile:
    """Estructura de un DBF

    Ejemplo:
        with open("data.dbf", "rb") as f:
            dbfile = DBFile(f.read())
    """

    def __init__(self, data: bytes):

        version, y, m, d, numrec, lenheader, lenrecord = struct.unpack(
            b"<4BIHH20x", data[:32]
        )

        self.version: int = version
        self.desc: str = dbf_version(version)
        self.last_mod: datetime.date = datetime.date(
            year=1900 + y, month=m, day=d
        )
        self.numrec: int = numrec
        self.lenheader: int = lenheader

        term = data[lenheader - 1]
        if term != 0x0D:
            raise Exception(f"Header must ends with '0x0d' (not '{term:#x}')")

        self.header = data[:lenheader]
        self.records = data[lenheader:]

    @property
    def is_implemented(self) -> bool:
        return self.version in _IMPLEMENTED

    @property
    def numfields(self):

        if self.version == 0x04:  # dBASE 7
            return (self.lenheader - 69) // 48
        else:
            # TODO: NOT IMPLEMENTED
            return (self.lenheader - 33) // 32

    def fields(self):

        if self.version not in _IMPLEMENTED:
            raise NotImplementedError

        start = 68
        stop = self.lenheader - 1
        for fieldpos in range(start, stop, 48):
            field = self.header[fieldpos : fieldpos + 48]  # noqa: E203
            name, typ, size, deci = struct.unpack(b"<32scBB13x", field)
            name = b2str(name)
            typ = typ.decode()
            yield (name, typ, size, deci)

    def rows(self):

        if self.version not in _IMPLEMENTED:
            raise NotImplementedError

        fds = [("DeletionFlag", "C", 1, 0)] + list(self.fields())
        fmt = "".join("%ds" % fieldinfo[2] for fieldinfo in fds)
        fmtsiz = struct.calcsize(fmt)

        stop = len(self.records) - 1
        for rowpos in range(0, stop, fmtsiz):
            row = self.records[rowpos : rowpos + fmtsiz]  # noqa: E203
            record = struct.unpack(fmt, row)
            if record[0] != b" ":
                continue  # deleted record
            result = []
            for (name, typ, size, deci), value in zip(fds, record):
                if name == "DeletionFlag":
                    continue
                if typ == "C":
                    value = b2str(value, "latin1")
                elif typ == "N":
                    value = value.replace("\0", "").lstrip()
                    if value == "":
                        value = 0
                    elif deci:
                        value = decimal.Decimal(value)
                    else:
                        value = int(value)
                elif typ == "D":
                    y, m, d = int(value[:4]), int(value[4:6]), int(value[6:8])
                    value = datetime.date(y, m, d)
                elif typ == "L":
                    value = (
                        (value in "YyTt" and "T")
                        or (value in "NnFf" and "F")
                        or "?"
                    )
                result.append(value)
            yield result

    def to_csv(self, fname: Union[str, Path]):
        fieldnames = [field[0] for field in self.fields()]

        with open(fname, "w", newline="", encoding="utf8") as g:
            writer = csv.writer(g, quoting=csv.QUOTE_MINIMAL)
            writer.writerow(fieldnames)
            writer.writerows(self.rows())
