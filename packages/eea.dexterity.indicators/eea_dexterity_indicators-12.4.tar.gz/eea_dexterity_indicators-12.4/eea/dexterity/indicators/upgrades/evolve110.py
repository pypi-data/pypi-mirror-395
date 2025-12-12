"""Upgrade step to upgrade indicators to the new embed block"""

from Products.CMFCore.utils import getToolByName
from Products.ZCatalog.ProgressHandler import ZLogHandler
from plone.restapi.blocks import visit_blocks


def to_110(context):
    """Upgrade all dataFigure blocks to embed_content"""
    ctool = getToolByName(context, "portal_catalog")
    brains = ctool.unrestrictedSearchResults(portal_type="ims_indicator")
    pghandler = ZLogHandler(100)
    pghandler.init("Convert dataFigure to embed_content blocks", len(brains))
    for idx, brain in enumerate(brains):
        pghandler.report(idx)
        doc = brain.getObject()
        for block in visit_blocks(doc, doc.blocks):
            block_type = block.get("@type", "")
            if block_type == "dataFigure":
                block["old_type"] = block_type
                block["@type"] = "embed_content"
                block["with_metadata_section"] = True
                block["svg_as_img"] = True
                block["with_notes"] = False
                href = block.get("href", "")
                if href and "/resolveuid/" in href:
                    block["old_url"] = block.get("url", "")
                    block["url"] = href
                doc.reindexObject()
    pghandler.finish()
