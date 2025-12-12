"""Custom behavior for Indicator"""

from eea.dexterity.indicators.interfaces import IIndicatorMetadata
from zope.component import adapter
from zope.interface import implementer
from plone import api
from plone.dexterity.interfaces import IDexterityContent
from plone.restapi.blocks import visit_blocks


def remove_api_string(url):
    """
    Remove /api/SITE/ or ++api++ substring from url

    Args:
        url (str): url string
    """
    url = url.replace("/api/SITE/", "/")
    url = url.replace("/++api++/", "/")
    url = url.strip("/").strip("/view")
    return url


def dedupe_data(data):
    """
    Remove duplication from metadata fields on basis of url fields or title
    for items without links

    >>> from eea.dexterity.indicators.behaviors.indicator import dedupe_data
    >>> value=[{"link": "https://www.eea.europa.eu", "title": "title"},
    ... {"link": "https://www.eea.europa.eu/", "title": "title 2"}]
    >>> result = dedupe_data(value)
    >>> [ x['link'] for x in result]
    ['https://www.eea.europa.eu']

    """
    existing_urls = set()
    existing_titles = set()

    for value in data:
        url = value.get("link", "")
        title = value.get("title", "")

        if url:
            url = remove_api_string(url)
            if url in existing_urls:
                continue
            existing_urls.add(url)
        elif title and title in existing_titles:
            continue

        if title:
            existing_titles.add(title)

        yield value


def get_embed_content(block):
    """Get related content from block"""
    path = block.get("url", "")
    if not path:
        return None
    if path.startswith("http"):
        return None
    if path.startswith("/api/SITE/"):
        return None
    if "resolveuid/" in path:
        uid = path.split("resolveuid/")[-1]
        return api.content.get(UID=uid)
    return api.content.get(path=path)


@implementer(IIndicatorMetadata)
@adapter(IDexterityContent)
class Indicator:
    """Automatically extract metadata from blocks"""

    def __init__(self, context):
        self.__dict__["context"] = context
        self.__dict__["readOnly"] = [
            "temporal_coverage",
            "geo_coverage",
            "data_provenance",
        ]

    def __getattr__(self, name):
        if name not in IIndicatorMetadata:
            raise AttributeError(name)

        if name not in self.__dict__["readOnly"]:
            return getattr(
                self.__dict__.get("context"),
                name,
                IIndicatorMetadata[name].missing_value,
            )

    def __setattr__(self, name, value):
        if name not in IIndicatorMetadata:
            raise AttributeError(name)

        if name not in self.__dict__["readOnly"]:
            setattr(self.context, name, value)

    @property
    def temporal_coverage(self):
        """Get temporal coverage from Data figure blocks"""
        res = {"readOnly": True, "temporal": []}
        temporal = []
        blocks = getattr(self.context, "blocks", None) or {}
        for block in visit_blocks(self.context, blocks):
            block_temporal = block.get("temporal", None)
            if block_temporal is not None:
                for item in block_temporal:
                    if item not in temporal:
                        temporal.append(item)
                continue

            if block.get("@type", "") == "embed_content":
                content = get_embed_content(block)
                temporal_coverage = getattr(content, "temporal_coverage", {})
                block_temporal = temporal_coverage.get("temporal", [])
                for item in block_temporal:
                    if item not in temporal:
                        temporal.append(item)

        res["temporal"] = sorted(temporal, key=lambda x: x.get("label"))
        return res

    @property
    def geo_coverage(self):
        """Get geo coverage from Data figure blocks"""
        res = {"readOnly": True, "geolocation": []}
        geolocation = []
        blocks = getattr(self.context, "blocks", None) or {}
        for block in visit_blocks(self.context, blocks):
            block_geolocation = block.get("geolocation", None)
            if block_geolocation is not None:
                for item in block_geolocation:
                    geo_item = {
                        "label": item.get("label", ""),
                        "value": item.get("value", ""),
                    }
                    if geo_item not in geolocation:
                        geolocation.append(geo_item)
                continue

            if block.get("@type", "") == "embed_content":
                content = get_embed_content(block)
                geo_coverage = getattr(content, "geo_coverage", {})
                block_geo = geo_coverage.get("geolocation", None)
                if not block_geo:
                    continue

                for item in block_geo:
                    geo_item = {
                        "label": item.get("label", ""),
                        "value": item.get("value", ""),
                    }
                    if geo_item not in geolocation:
                        geolocation.append(geo_item)

        res["geolocation"] = sorted(geolocation, key=lambda x: x.get("label"))
        return res

    @property
    def data_provenance(self):
        """Data sources and providers"""
        res = []
        blocks = getattr(self.context, "blocks", None) or {}
        for block in visit_blocks(self.context, blocks):
            if "data_provenance" in block:
                data_provenance = block.get("data_provenance", {}).get("data", []) or []
                res.extend(data_provenance)
                continue

            if block.get("@type", "") == "embed_content":
                content = get_embed_content(block)
                data_provenance = getattr(content, "data_provenance", {})
                if data_provenance:
                    data_provenance = data_provenance.get("data", []) or []
                    res.extend(data_provenance)

        return {"readOnly": True, "data": list(dedupe_data(res))}
