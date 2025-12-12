"""
This module contains internal helper functions for extracting and merging journal metrics
"""
from bibliometria.journal_data import get_sjr, get_wos, items1, items2, issn_idx1, issn_idx2
from bibliometria.data_utils import _split_codes, _normalize_issn

import pandas as pd
from rapidfuzz import fuzz, process


df1 = get_sjr()
df2 = get_wos()


def _extract_metrics_from_row(row):
    """
    Takes a row and returns only the relevant metrics:
      SJR (df1): sjr, sjr_best_quartile, h_index
      WoS (df2): wos_quartile, wos_jif, wos_jif_5_year
    Missing values → None.
    """
    sjr_cols = ['sjr', 'sjr_best_quartile', 'h_index']
    wos_cols = ['wos_quartile', 'wos_jif', 'wos_jif_5_year']

    data = {c: None for c in (sjr_cols + wos_cols)}
    if row is None:
        return pd.Series(data)

    # transfer only the fields that exist in this row
    for c in data.keys():
        if c in row.index and pd.notna(row[c]):
            data[c] = row[c]
    return pd.Series(data)


def _find_partner_row(row, source):
    if row is None:
        return None

    codes = []
    if "issn" in row.index:  codes += _split_codes(row["issn"])
    if "eissn" in row.index: codes += _split_codes(row["eissn"])

    def variants(code):
        n = _normalize_issn(code)
        return [n, n.replace('-', ''), str(code).strip().upper()]

    if source == "df1":
        for code in codes:
            for key in variants(code):
                if key in issn_idx2:
                    return df2.loc[issn_idx2[key]]
    else:  # source == "df2"
        for code in codes:
            for key in variants(code):
                if key in issn_idx1:
                    return df1.loc[issn_idx1[key]]

    return None


def _merge_metric_parts(left_part, right_part):
    """
    Merges two Series of metrics (priority: non-None).
    Expects identical indices: sjr, sjr_best_quartile, h_index,
                              wos_quartile, wos_jif, wos_jif_5_year.
    """
    keys = ['sjr','sjr_best_quartile','h_index','wos_quartile','wos_jif','wos_jif_5_year']
    out = pd.Series({k: None for k in keys})
    for k in keys:
        v1 = left_part.get(k)
        v2 = right_part.get(k)
        out[k] = v1 if pd.notna(v1) else v2
    return out


def _get_row_by_issn(code):
    """
    Searches ISSN/eISSN in both datasets (SJR=df1, WoS=df2)
    and returns a Series with combined metrics.

    Metrics:
      from SJR (df1): sjr, sjr_best_quartile, h_index
      from WoS (df2): wos_quartile, wos_jif, wos_jif_5_year

    If the ISSN/eISSN is not found in the dataset — the corresponding fields = None.
    """
    # no value provided
    if code is None:
        return pd.Series({
            "issn": None,
            "sjr": None, "sjr_best_quartile": None, "h_index": None,
            "wos_quartile": None, "wos_jif": None, "wos_jif_5_year": None
        })

    q = str(code).strip()
    if not q or q == "-":
        return pd.Series({
            "issn": None,
            "sjr": None, "sjr_best_quartile": None, "h_index": None,
            "wos_quartile": None, "wos_jif": None, "wos_jif_5_year": None
        })

    # get rows from both sources (if available)
    row1 = df1.loc[issn_idx1[q]] if q in issn_idx1 else None
    row2 = df2.loc[issn_idx2[q]] if q in issn_idx2 else None

    # gather metrics
    sjr_cols = ["sjr", "sjr_best_quartile", "h_index"]
    wos_cols = ["wos_quartile", "wos_jif", "wos_jif_5_year"]

    data = {"issn": q}

    # SJR metrics (from df1 only)
    for c in sjr_cols:
        data[c] = (row1[c] if (row1 is not None and c in row1 and pd.notna(row1[c])) else None)

    # WoS metrics (from df2 only)
    for c in wos_cols:
        data[c] = (row2[c] if (row2 is not None and c in row2 and pd.notna(row2[c])) else None)

    return pd.Series(data)


def _get_row_by_title(title_query):
    """
    Returns (row, source, matched_title, score) based on the best fuzzy title match.
    """
    best = _title_best_match(title_query)
    if best is None:
        return None, None, None, None
    
    idx, matched_title, score, source = best
    row = (df1 if source == "df1" else df2).loc[idx].copy()
    return row, source, matched_title, score


def _title_best_match(
    title_query: str
) -> tuple[int, str, float, str] | None:
    """
    Find the single best title candidate by fuzzy matching across SJR and WoS datasets.

    Parameters
    ----------
    title_query : str
        Journal title to match against two datasets

    Returns
    -------
    tuple[int, str, int, str] or None
        (row_idx, matched_title, score, source) for the best match, or None if no match is found.

    """

    if not isinstance(title_query, str):
        raise TypeError(f"title_query must be str, got {type(title_query).__name__}")

    r1 = process.extractOne(title_query, items1, scorer=_scorer)
    r2 = process.extractOne(title_query, items2, scorer=_scorer)

    best = None
    if r1 is not None:
        (idx1, t1), s1, _ = r1
        best = (idx1, t1, s1, "df1")
    if r2 is not None:
        (idx2, t2), s2, _ = r2
        if best is None or s2 > best[2]:
            best = (idx2, t2, s2, "df2")

    return best

def _scorer(query, choice, **kwargs):
    # choice = (issn, title)
    return fuzz.token_sort_ratio(query, choice[1])