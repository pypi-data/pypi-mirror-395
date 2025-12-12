"""
This module provides loading and indexing utilities for the built-in datasets with journal data
"""
from bibliometria.data_utils import _calculate_quartile, _check_title, _split_codes, _add_index_entry

import pandas as pd
import importlib.resources
import os

# for efficiency: cache for loaded datasets 
_sjr_data = None
_wos_data = None


def _load_csv(filename):
    """ Load CSV file from package data """
    # modern approach for Python 3.9+
    try:
        with importlib.resources.files("bibliometria.data").joinpath(filename).open() as f:
            return pd.read_csv(f)
    except (AttributeError, FileNotFoundError):
        # fallback for older Python
        try:
            with importlib.resources.open_text("bibliometria.data", filename) as f:
                return pd.read_csv(f)
        except (FileNotFoundError, ModuleNotFoundError):
            # development fallback
            data_path = os.path.join(os.path.dirname(__file__), 'data', filename)
            return pd.read_csv(data_path)


def get_sjr():
    """ Get SJR 2024 data (cached) """
    global _sjr_data
    if _sjr_data is None:
        _sjr_data = _load_csv('sjr_journals_2024.csv')
    return _sjr_data


def get_wos():
    """ Get WOS data (cached) """
    global _wos_data
    if _wos_data is None:
        _wos_data = _load_csv('wos_journals.csv')
    return _wos_data


df1 = get_sjr()
df2 = get_wos()

# compute WoS quartile if the column exists
if "percentage" in df2.columns:
    df2["wos_quartile"] = df2["percentage"].apply(_calculate_quartile)
else:
    df2["wos_quartile"] = None  # column still exists for uniformity

# list of pairs: row index, journal title
items1 = list(zip(df1.index.tolist(),
                  # extract all row indices from df1; if column absent — use empty strings
                  [_check_title(x) for x in (df1["title"] if "title" in df1.columns else [""] * len(df1))]))
items2 = list(zip(df2.index.tolist(),
                  [_check_title(x) for x in (df2["title"] if "title" in df2.columns else [""] * len(df2))]))

# dictionaries: key = ISSN, value = row index
# df1 (SJR)
issn_idx1 = {}
if "issn" in df1.columns:
    for i, cell in df1["issn"].items():
        for code in _split_codes(cell):
            _add_index_entry(issn_idx1, code, i)

# df2 (WoS)
issn_idx2 = {}
if "issn" in df2.columns:
    for i, cell in df2["issn"].items():
        _add_index_entry(issn_idx2, cell, i)
if "eissn" in df2.columns:
    for i, cell in df2["eissn"].items():
        _add_index_entry(issn_idx2, cell, i)