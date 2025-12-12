"""
This module contains internal helper functions for processing journal data.
"""
import re
import pandas as pd


# if there are 2 values — extract them into a list
def _split_codes(x):
    """'1234-5678, 8765-4321' -> ['1234-5678','8765-4321']; skips empty/'-'."""
    if pd.isna(x):
        return []
    out = []
    for p in str(x).split(","):
        p = p.strip()
        if p and p != "-":
            out.append(p)
    return out

def _normalize_issn(code):
    """
    Converts ISSN into standard ####-#### format. Keeps X as a valid check digit.
    '22959149' -> '2295-9149'
    '2649664X' -> '2649-664X'
    """
    s = str(code).strip().upper()
    s = re.sub(r'[^0-9X]', '', s)  # keep only digits and X
    if len(s) == 8:
        return f"{s[:4]}-{s[4:]}"
    return s  # if length is not 8 — return as it is

def _check_title(x):
    """Ensures each cell is a string, even if it contains NaN."""
    if pd.isna(x):
        return ""
    return str(x)

# calculate quartile based on the WoS formula (Q1 ≥ 75, Q2 ≥ 50, Q3 ≥ 25, else Q4)
def _calculate_quartile(p):
    if pd.isna(p):
        return None
    s = str(p).strip()
    # remove percent sign and exotic variants
    s = s.replace('%', '').replace('％', '')
    # replace comma with dot and remove internal spaces
    s = s.replace(',', '.').replace(' ', '')
    try:
        v = float(s)
    except Exception:
        return None
    # if it is a fraction (e.g. 0.997), treat it as 99.7%
    if v <= 1.5:
        v *= 100.0
    if v >= 75:
        return "Q1"
    if v >= 50:
        return "Q2"
    if v >= 25:
        return "Q3"
    return "Q4"

def _add_index_entry(dct, code, row_idx):
    # normalized, no-dash version + original version
    norm = _normalize_issn(code)
    variants = {norm, norm.replace('-', ''), str(code).strip().upper()}
    for k in variants:
        if k:
            dct.setdefault(k, row_idx)