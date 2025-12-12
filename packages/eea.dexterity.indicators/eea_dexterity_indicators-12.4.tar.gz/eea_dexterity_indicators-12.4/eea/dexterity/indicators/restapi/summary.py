"""
Patch JSON Summary Serializer (Copied from plone.restapi 8.x)

To be removed when switched to plone.restapi >= 8.x
"""

from plone.restapi.serializer.summary import DefaultJSONSummarySerializer
from plone.restapi.interfaces import ISerializeToJsonSummary
from plone.restapi.deserializer import json_body
from zope.component import adapter
from zope.interface import implementer
from zope.interface import Interface
from eea.dexterity.indicators.interfaces import IEeaDexterityIndicatorsLayer


@implementer(ISerializeToJsonSummary)
@adapter(Interface, IEeaDexterityIndicatorsLayer)
class BackportJSONSummarySerializer(DefaultJSONSummarySerializer):
    """Backport ISerializeToJsonSummary adapter."""

    def metadata_fields(self):
        """Fields"""
        if not self.request.form:
            # maybe its a POST request
            query = json_body(self.request)
            self.request.form["metadata_fields"] = query.get("metadata_fields", [])
        return super().metadata_fields()
