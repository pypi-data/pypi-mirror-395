"""
Bibliometria: A package for bibliometric analysis of journals.

This package provides tools for retrieving journal information and comparing metrics,  
combining the data from SCImago Journal Rank (SJR) and Web of Science (WoS). 

Features

Data access
----------
- get_sjr()
    Return the built-in SJR table as a pandas.DataFrame.
- get_wos()
    Return the built-in WoS table as a pandas.DataFrame.

Title matching
----------
- title_matches(title_query, limit=10, score_cutoff=60)
    Find top-N fuzzy matches for a journal title across SJR and WoS.
- title_best_match(title_query)
    Return a concise Series describing the single best fuzzy match.

Journal metrics
----------
- journal_metrics(query, query_type="title")
    Return a Series with core SJR/WoS metrics for a journal.
- journal_info(query, query_type="title")
    Return a single-row DataFrame with all available SJR/WoS fields
    and matching metadata.
"""

__version__ = "0.1.0"
__license__ = "GPL-3.0"

from .journal_data import get_sjr, get_wos
from .metrics import (
    title_matches,
    title_best_match,
    journal_metrics,
    journal_info,
)

__all__ = [
    "__version__",
    "__license__",
    "get_sjr",
    "get_wos",
    "title_matches",
    "title_best_match",
    "journal_metrics",
    "journal_info",
]