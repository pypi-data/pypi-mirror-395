"""
This module provides four main user functions of the package.
"""

from bibliometria.data_utils import _normalize_issn
from bibliometria.journal_data import get_sjr, get_wos, items1, items2, issn_idx1, issn_idx2
from bibliometria.metrics_utils import _extract_metrics_from_row, _find_partner_row, _merge_metric_parts, _get_row_by_title, _title_best_match, _scorer

import pandas as pd
from rapidfuzz import process
import warnings


df1 = get_sjr()
df2 = get_wos()


def title_matches(
    title_query: str,
    limit: int = 10,
    score_cutoff: int = 60
) -> pd.DataFrame:
    """
    Find top-n title candidates by fuzzy matching across SJR and WoS datasets.

    Parameters
    ----------
    title_query : str
        Journal title to match against two datasets.
    limit : int, optional
        Maximum number of candidates to retrieve.
    score_cutoff : int, optional
        Minimal similarity score for a match to be included.

    Returns
    -------
    pandas.DataFrame
        Each row is a candidate match with similarity score and journal metadata.
        May be empty if no candidates satisfy score_cutoff.
    """
    if not isinstance(title_query, str):
        raise TypeError(f"title_query must be str, got {type(title_query).__name__}")
    if not isinstance(limit, int):
        raise TypeError(f"limit must be int, got {type(limit).__name__}")
    if not isinstance(score_cutoff, int):
        raise TypeError(f"score_cutoff must be int, got {type(score_cutoff).__name__}")

    rows = []

    r1 = process.extract(title_query, items1, scorer=_scorer, limit=limit, score_cutoff=score_cutoff)
    for (idx, t), s, _ in r1:
        row = df1.loc[idx].copy()
        row["raw_title"] = title_query
        row["matched_title"] = t
        row["match_score"] = round(float(s), 2)
        row["source"] = "SCImagojr"
        rows.append(row)

    r2 = process.extract(title_query, items2, scorer=_scorer, limit=limit, score_cutoff=score_cutoff)
    for (idx, t), s, _ in r2:
        row = df2.loc[idx].copy()
        row["raw_title"] = title_query
        row["matched_title"] = t
        row["match_score"] = round(float(s), 2)
        row["source"] = "Web of Science"
        rows.append(row)

    if not rows:
        return pd.DataFrame(columns=[
            "raw_title","matched_title","match_score","source",
            "title","issn","eissn","sjr","sjr_best_quartile","wos_quartile"
        ])

    result = pd.DataFrame(rows).sort_values("match_score", ascending=False)

    result = result.head(limit)
    result = result.reset_index(drop=True)

    order = [
        "raw_title", "matched_title", "match_score", "source", "title", 
        "issn", "eissn", "sjr", "sjr_best_quartile", "wos_quartile",
    ]
    cols = [c for c in order if c in result.columns] 
    
    return result[cols]


def title_best_match(
    title_query: str
) -> pd.Series | None:
    """
    Find the single best title candidate by fuzzy matching across SJR and WoS datasets.

    Parameters
    ----------
    title_query : str
        Journal title to match against two datasets

    Returns
    -------
    pandas.Series or None
        A Series with fields such as:
        raw_title, matched_title, match_score, source, title, issn, eissn, ...
        or None if no match is found.
    """

    if not isinstance(title_query, str):
        raise TypeError(f"title_query must be str, got {type(title_query).__name__}")

    best = _title_best_match(title_query)
    if best is None:
        return None

    idx, matched_title, score, source = best
    base_df = df1 if source == "df1" else df2
    row = base_df.loc[idx].copy()

    row["raw_title"] = title_query
    row["matched_title"] = matched_title
    row["match_score"] = float(score)
    row["source"] = "SCImagojr" if source == "df1" else "Web of Science"


    order = [
        "raw_title", "matched_title", "match_score", "source",
        "title", "issn", "eissn", "sjr", "sjr_best_quartile", "wos_quartile"
    ]
    cols = [c for c in order if c in row.index]

    return pd.Series({c: row[c] for c in cols})


def journal_metrics(
    query: str | int,
    query_type: str = "title"
) -> pd.Series:

    """
    Find core SJR and WoS metric values for a journal by title or ISSN.

    Parameters
    ----------
    query : str or int
        Journal title or ISSN/eISSN.
    query_type : str, optional
        Searching mode, either "title" (fuzzy match) or "issn" (exact match).

    Returns
    -------
    pandas.Series
        Series with metrics sjr, sjr_best_quartile, h_index, wos_quartile, wos_jif, wos_jif_5_year;
        Series.name contains the matched journal title or None if not found.
        May be empty if the journal was not found.
    """

    if not isinstance(query, (str, int)):
        raise TypeError(f"Invalid query: must be str or int, got {type(query).__name__}")
    if query_type not in {"title", "issn"}:
        raise ValueError(f"Invalid query_type: must be 'title' or 'issn', got {query_type}")


    empty = pd.Series({
        'sjr': None, 'sjr_best_quartile': None, 'h_index': None,
        'wos_quartile': None, 'wos_jif': None, 'wos_jif_5_year': None
    })

    # ISSN
    if query_type == "issn":
        q = str(query).strip()
        # use only valid issn
        norm = _normalize_issn(q)
        digits = norm.replace("-", "")

        if len(digits) != 8:
            raise ValueError(f"Invalid ISSN format: {query!r}.")

        # check both formats
        issn_keys = {norm, digits}

        row1 = None
        row2 = None
        for k in issn_keys:
            if row1 is None and k in issn_idx1:
                row1 = df1.loc[issn_idx1[k]]
            if row2 is None and k in issn_idx2:
                row2 = df2.loc[issn_idx2[k]]

        if (row1 is None) and (row2 is None):
            warnings.warn("Journal was not found by this ISSN.", RuntimeWarning)
            empty.name = None
            return empty

        sjr_part = _extract_metrics_from_row(row1)
        wos_part = _extract_metrics_from_row(row2)

        result = empty.copy()
        for k in result.index:
            v1 = sjr_part.get(k)
            v2 = wos_part.get(k)
            result[k] = v1 if pd.notna(v1) else v2

        # title for Series.name: prefer df1, fallback to df2
        title = None
        if row1 is not None and "title" in row1.index and pd.notna(row1["title"]):
            title = row1["title"]
        elif row2 is not None and "title" in row2.index and pd.notna(row2["title"]):
            title = row2["title"]

        result.name = title
        
        return result
        
    # title (fuzzy)
    elif query_type == "title":
        row, source, matched_title, score = _get_row_by_title(query)
        if row is None:
            empty.name = None
            warnings.warn("Journal was not found for this title query.", RuntimeWarning)
            return empty

        primary_part = _extract_metrics_from_row(row)
        partner_row = _find_partner_row(row, source)
        partner_part = _extract_metrics_from_row(
            partner_row
        )

        result = _merge_metric_parts(primary_part, partner_part)

        # heading - the matched journal title
        result.name = matched_title if matched_title is not None else str(query)

        # warn if fuzzy score < 100
        if score is not None and score < 100:
            warnings.warn(
                f"Identical title was not found, showing results for the match with similarity {score:.0f}%. "
                f"Matched journal: '{matched_title}'.", RuntimeWarning)

    return result


def journal_info(
    query: str | int,
    query_type: str = "title"
) -> pd.DataFrame:

    """
    Return a single-row table with all available data from SJR and WoS for a journal by title or ISSN.

    Parameters
    ----------
    query : str or int
        Journal title or ISSN/eISSN.
    query_type : str, optional
        Searching mode, either "title" (fuzzy match) or "issn" (exact match).

    Returns
    -------
    pandas.DataFrame
        Single-row DataFrame with all merged data from SJR/WoS and metadata
        (query, query_type, source_primary, matched_title, match_score).
        If no journal is found, contains only metadata values, other are None.
    """
    
    if not isinstance(query, (str, int)):
        raise TypeError(f"Invalid query: must be str or int, got {type(query).__name__}")
    if query_type not in {"title", "issn"}:
        raise ValueError(f"Invalid query_type: must be 'title' or 'issn', got {query_type}")


    # helper to wrap a merged Series into a DataFrame
    def _wrap_single_row(merged_row,
                         query_val,
                         query_type_val,
                         source_primary,
                         matched_title,
                         score):
        # if nothing exists — return a minimal structure
        if merged_row is None:
            df = pd.DataFrame([{
                "query": query_val,
                "query_type": query_type_val,
                "source_primary": source_primary,
                "matched_title": matched_title,
                "match_score": score
            }])
        else:
            df = merged_row.to_frame().T
            # insert metadata fields at the beginning
            df.insert(0, "query", query_val)
            df.insert(1, "query_type", query_type_val)
            df.insert(2, "source_primary", source_primary)
            df.insert(3, "matched_title", matched_title)
            df.insert(4, "match_score", score)

        # make title the first column if present
        if "title" in df.columns:
            cols = list(df.columns)
            cols.remove("title")
            df = df[["title"] + cols]

        return df

    # ISSN 
    if query_type == "issn":
        q = str(query).strip()
        # use only valid issn
        norm = _normalize_issn(q)
        digits = norm.replace("-", "")

        if len(digits) != 8:
            raise ValueError(f"Invalid ISSN format: {query!r}.")

        # check both formats
        issn_keys = {norm, digits}

        row1 = None
        row2 = None
        for k in issn_keys:
            if row1 is None and k in issn_idx1:
                row1 = df1.loc[issn_idx1[k]]
            if row2 is None and k in issn_idx2:
                row2 = df2.loc[issn_idx2[k]]

        if (row1 is None) and (row2 is None):
            warnings.warn("Journal was not found by this ISSN.", RuntimeWarning)
            return _wrap_single_row(
                merged_row=None,
                query_val=query,
                query_type_val="issn",
                source_primary=None,
                matched_title=None,
                score=None
            )

        if (row1 is not None) or (row2 is not None):
            # merge row1 + row2 
            if row1 is not None:
                merged = row1.copy()
                if row2 is not None:
                    for c in row2.index:
                        if (c not in merged.index) or pd.isna(merged[c]):
                            merged[c] = row2[c]
                source_primary = "SCImagojr"
            else:
                merged = row2.copy()
                source_primary = "Web of Science"

            # exact match => score 100
            result = _wrap_single_row(
                merged_row=merged,
                query_val=query,
                query_type_val="issn",
                source_primary=source_primary,
                matched_title=merged.get("title") if merged is not None else None,
                score=100
            )
            return result


    # title (fuzzy)
    elif query_type == "title":
        row, source, matched_title, score = _get_row_by_title(query)
        if row is None:
            warnings.warn("Journal was not found for this title query.", RuntimeWarning)
            return _wrap_single_row(
                merged_row=None,
                query_val=query,
                query_type_val="title",
                source_primary=None,
                matched_title=None,
                score=None
            )

        partner_row = _find_partner_row(row, source)

        # merge row + partner_row
        if row is not None:
            merged = row.copy()
            if partner_row is not None:
                for c in partner_row.index:
                    if (c not in merged.index) or pd.isna(merged[c]):
                        merged[c] = partner_row[c]
        else:
            merged = partner_row.copy() if partner_row is not None else None

        if score is not None and score < 100:
            warnings.warn(
                f"Identical title was not found, showing results for the match with similarity {score:.0f}%. "
                f"Matched journal: '{matched_title}'.", RuntimeWarning)

        result = _wrap_single_row(
            merged_row=merged,
            query_val=query,
            query_type_val="title",
            source_primary=source,
            matched_title=matched_title,
            score=score
        )


    return result