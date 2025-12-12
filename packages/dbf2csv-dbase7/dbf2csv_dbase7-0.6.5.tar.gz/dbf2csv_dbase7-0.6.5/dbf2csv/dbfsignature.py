"""
Versión fichero DBF

A partir del primer byte del fichero dbf se obtiene la versión de la aplicación
dbBASE a la que pertenece

Byte 0
-----------
x xxx x 001 = 0x01 not used
0 000 0 010 = 0x02 FoxBASE
0 000 0 011 = 0x03 FoxBASE+/dBASE III PLUS, no memo
x xxx x 100 = 0x04 dBASE 7
0 000 0 101 = 0x05 dBASE 5, no memo
0 011 0 000 = 0x30 Visual FoxPro
0 011 0 001 = 0x31 Visual FoxPro, autoincrement enabled
0 011 0 010 = 0x32 Visual FoxPro, Varchar, Varbinary, or Blob-enabled
0 100 0 011 = 0x43 dBASE IV SQL table files, no memo
0 110 0 011 = 0x63 dBASE IV SQL system files, no memo
0 111 1 011 = 0x7B dBASE IV, with memo
1 000 0 011 = 0x83 FoxBASE+/dBASE III PLUS, with memo
1 000 1 011 = 0x8B dBASE IV, with memo
1 000 1 110 = 0x8E dBASE IV with SQL table
1 100 1 011 = 0xCB dBASE IV SQL table files, with memo
1 110 0 101 = 0xE5 Clipper SIX driver, with SMT memo
1 111 0 101 = 0xF5 FoxPro 2.x (or earlier) with memo
1 111 1 011 = 0xFB FoxBASE (with memo?)
| ||| | |||
| ||| | |||   Bit flags (not used in all formats)
| ||| | |||   -----------------------------------
| ||| | +++-- bits 2, 1, 0, version (x03 = level 5, x04 = level 7)
| ||| +------ bit 3, presence of memo file
| +++-------- bits 6, 5, 4, presence of dBASE IV SQL table
+------------ bit 7, presence of .DBT file
"""

SIGNATURES = {
    0x02: "FoxBASE",
    0x03: "FoxBASE+/dBASE III PLUS, no memo",
    0x04: "dBASE 7",
    0x05: "dBASE 5, no memo",
    0x30: "Visual FoxPro",
    0x31: "Visual FoxPro, autoincrement enabled",
    0x32: "Visual FoxPro, Varchar, Varbinary, or Blob-enabled",
    0x43: "dBASE IV SQL table files, no memo",
    0x63: "dBASE IV SQL system files, no memo",
    0x7B: "dBASE IV, with memo",
    0x83: "FoxBASE+/dBASE III PLUS, with memo",
    0x8B: "dBASE IV, with memo",
    0x8E: "dBASE IV with SQL table",
    0xCB: "dBASE IV SQL table files, with memo",
    0xE5: "Clipper SIX driver, with SMT memo",
    0xF5: "FoxPro 2.x (or earlier) with memo",
    0xFB: "FoxBASE (with memo?)",
}


def dbf_version(n: int) -> str:
    return SIGNATURES.get(n, "UNKNOWN VERSION")
