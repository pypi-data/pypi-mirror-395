#!/usr/bin/env python

import sys
from pathlib import Path

from dbf2csv.dbfreader import DBFile


def usage() -> str:
    return """
    | dbf2csv - Conversor de DBF a CSV
    |
    | Uso:
    |    dbf2csv dbf_file <csv_file>
    """.replace(
        "    |", ""
    )


def convert(dbf_file: Path, csv_file: "Path | None" = None) -> "int | str":

    if not dbf_file.exists():
        return f"ERROR: Fichero {dbf_file} no encontrado"

    if not csv_file:
        csv_file = dbf_file.with_suffix(".csv")

    db = DBFile(dbf_file.read_bytes())
    print(f"\nFichero DBF '{dbf_file}' ({db.desc})")
    print(f"Tamaño: {db.numrec} registros")
    print(f"Última modificación: {db.last_mod}")
    if not db.is_implemented:
        return f"\n\nFORMATO '{db.desc}' NO IMPLEMENTADO TODAVÍA"

    print(f"Conversión {dbf_file} --> {csv_file}")
    print(f"\nCreado fichero '{csv_file}'")
    db.to_csv(csv_file)

    return 0


def run() -> "int | str":

    if len(sys.argv) <= 1:
        print(usage())
        return "ERROR: No he recibido ningún fichero DBF para convertir"
    elif len(sys.argv) == 2:
        dbf_file = Path(sys.argv[1])
        csv_file = None
    else:
        dbf_file = Path(sys.argv[1])
        csv_file = Path(sys.argv[2])

    if not dbf_file.exists():
        return f"ERROR: Fichero {dbf_file} no encontrado"

    return convert(dbf_file, csv_file)


if __name__ == "__main__":

    sys.exit(run())
