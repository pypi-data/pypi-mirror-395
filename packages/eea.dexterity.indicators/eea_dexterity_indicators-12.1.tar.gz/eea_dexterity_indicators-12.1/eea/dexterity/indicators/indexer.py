""" indexer.py """
from plone.indexer import indexer
from plone.base.utils import safe_text
from plone.app.contenttypes.indexers import SearchableText
from zope.component import queryAdapter
from eea.dexterity.indicators.interfaces import IIndicator
from eea.dexterity.indicators.interfaces import IIndicatorMetadata


def _unicode_save_string_concat(*args):
    """
    concats args with spaces between and returns utf-8 string, it does not
    matter if input was text or bytes
    """
    result = ""
    for value in args:
        if isinstance(value, bytes):
            value = safe_text(value)
        result = " ".join((result, value))
    return result


@indexer(IIndicator)
def searchable_text_indexer(obj):
    """SearchableText indexer"""
    return _unicode_save_string_concat(SearchableText(obj))


@indexer(IIndicator)
def data_provenance_indexer(obj):
    """Data Provenance indexer"""
    metadata = queryAdapter(obj, IIndicatorMetadata)
    if not metadata:
        return None
    data_provenance = getattr(metadata, "data_provenance", {})
    if not data_provenance or "data" not in data_provenance:
        return None

    data = {}
    for val in data_provenance['data']:
        org = val.get("organisation", "")
        if org:
            data[org] = org
    return data


@indexer(IIndicator)
def temporal_coverage_indexer(obj):
    """Temporal coverage indexer"""

    metadata = queryAdapter(obj, IIndicatorMetadata)
    if not metadata:
        return None
    temporal_coverage = getattr(metadata, "temporal_coverage", {})
    if not temporal_coverage or "temporal" not in temporal_coverage:
        return None

    data = {}
    for val in temporal_coverage["temporal"]:
        value = val.get("value", "")
        label = val.get("label", "")
        if value and label:
            data[value] = label
    return data
