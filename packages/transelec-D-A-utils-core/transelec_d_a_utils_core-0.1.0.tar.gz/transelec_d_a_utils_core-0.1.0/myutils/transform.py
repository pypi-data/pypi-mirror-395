# -*- coding: utf-8 -*-
import re
import unicodedata
from typing import List

def strip_accents(text: str) -> str:
    """Elimina acentos de un texto (Normalización NFKD)."""
    if text is None:
        return ""
    nfkd = unicodedata.normalize("NFKD", str(text))
    return "".join(c for c in nfkd if not unicodedata.combining(c))

def sql_name_strict(s: str) -> str:
    """
    Convierte un string en un nombre seguro y estricto para SQL/BigQuery.
    - Elimina acentos y convierte a mayúsculas.
    - Reemplaza caracteres no alfanuméricos por guion bajo (_).
    - Reemplaza "ANO" por "ANIO" como palabra completa.
    - Prefija con '_' si comienza con un dígito.
    """
    s = strip_accents(s).upper()
    s = re.sub(r"[^\w]+", "_", s)
    s = re.sub(r"_+", "_", s).strip("_")
    # ANO -> ANIO SOLO como palabra completa
    tokens = ["ANIO" if t == "ANO" else t for t in s.split("_")]
    s = "_".join(tokens)
    if s and s[0].isdigit():
        s = "_" + s
    return s or "COL"

def dedupe_names(names: List[str]) -> List[str]:
    """
    Añade un sufijo numérico (ej: _2, _3) a los nombres duplicados en una lista.
    Ej: [A, B, A] -> [A, B, A_2]
    """
    seen, out = {}, []
    for n in names:
        if n not in seen:
            seen[n] = 1
            out.append(n)
        else:
            seen[n] += 1
            out.append(f"{n}_{seen[n]}")
    return out

def file_safe_name(s: str, max_len: int = 90) -> str:
    """
    Convierte un string en un nombre seguro para un archivo.
    Permite caracteres alfanuméricos, guiones (-) y puntos (.).
    """
    s = strip_accents(str(s or "").strip())
    s = re.sub(r"[^\w\-.]+", "_", s)
    s = re.sub(r"_+", "_", s).strip("_.")
    return (s or "SERVICIO")[:max_len]