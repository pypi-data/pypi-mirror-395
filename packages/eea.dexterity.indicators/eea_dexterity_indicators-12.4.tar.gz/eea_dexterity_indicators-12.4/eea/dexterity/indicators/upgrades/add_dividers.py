"""Upgrade step to add new dividers to all indicators"""

from Products.CMFCore.utils import getToolByName
from Products.ZCatalog.ProgressHandler import ZLogHandler


def add_dividers_to_indicators(context):
    """Add new dividers to all indicators.

    Adds 43df8fab-b278-4b0e-a62c-ce6b8e0a881d and
    43df8fab-b278-4b0e-a62c-ce6b8e0a881e to all indicators.
    """
    ctool = getToolByName(context, "portal_catalog")
    brains = ctool.unrestrictedSearchResults(portal_type="ims_indicator")
    pghandler = ZLogHandler(100)
    pghandler.init("Add new dividers to all indicators", len(brains))

    # Define the new divider blocks
    new_dividers = {
        "43df8fab-b278-4b0e-a62c-ce6b8e0a881d": {
            "@type": "dividerBlock",
            "section": False,
            "short": True,
            "disableNewBlocks": True,
            "fixed": True,
            "hidden": True,
            "readOnly": True,
            "required": True,
            "styles": {},
            "spacing": "m",
            "fitted": False,
        },
        "43df8fab-b278-4b0e-a62c-ce6b8e0a881e": {
            "@type": "dividerBlock",
            "section": False,
            "short": True,
            "disableNewBlocks": True,
            "fixed": True,
            "hidden": True,
            "readOnly": True,
            "required": True,
            "spacing": "m",
            "fitted": False,
        },
    }

    def find_group_by_id_or_title(blocks, group_id, group_title):
        """Find group block by ID first, then by title"""
        # First try to find by ID
        if group_id in blocks:
            return blocks[group_id]

        # If not found by ID, search by title
        for block_data in blocks.values():
            if isinstance(block_data, dict) and block_data.get("title") == group_title:
                return block_data

        return None

    def add_divider_to_group(group, divider_id, embed_id, new_dividers):
        """Add divider to a group if it doesn't exist"""
        if not group or "data" not in group:
            return False

        group_data = group["data"]
        if "blocks" not in group_data:
            return False

        blocks = group_data["blocks"]

        # Add divider if it doesn't exist
        if divider_id in blocks:
            return False

        blocks[divider_id] = new_dividers[divider_id]

        # Add to layout if present
        if "blocks_layout" in group_data and "items" in group_data["blocks_layout"]:
            layout_items = group_data["blocks_layout"]["items"]
            if divider_id not in layout_items:
                # Insert after the embed_content block
                if embed_id in layout_items:
                    embed_index = layout_items.index(embed_id)
                    layout_items.insert(embed_index + 1, divider_id)
                else:
                    layout_items.append(divider_id)

        return True

    for idx, brain in enumerate(brains):
        pghandler.report(idx)
        doc = brain.getObject()

        # Check if the document has blocks
        if not hasattr(doc, "blocks") or not doc.blocks:
            continue

        blocks_modified = False

        # Find and update Aggregate level assessment group
        aggregate_id = "1bc4379d-cddb-4120-84ad-5ab025533b12"
        aggregate_title = "Aggregate level assessment"
        aggregate_group = find_group_by_id_or_title(
            doc.blocks, aggregate_id, aggregate_title
        )

        divider_id1 = "43df8fab-b278-4b0e-a62c-ce6b8e0a881d"
        embed_id1 = "b0279dde-1ceb-4137-a7f1-5ab7b46a782c"
        if add_divider_to_group(aggregate_group, divider_id1, embed_id1, new_dividers):
            blocks_modified = True

        # Find and update Disaggregate level assessment group
        disaggregate_id = "d060487d-88fc-4f7b-8ea4-003f14e0fb0c"
        disaggregate_title = "Disaggregate level assessment"
        disaggregate_group = find_group_by_id_or_title(
            doc.blocks, disaggregate_id, disaggregate_title
        )

        divider_id2 = "43df8fab-b278-4b0e-a62c-ce6b8e0a881e"
        embed_id2 = "02ba4a04-fcfe-4968-806f-1dac3119cfef"
        if add_divider_to_group(
            disaggregate_group, divider_id2, embed_id2, new_dividers
        ):
            blocks_modified = True

        if blocks_modified:
            doc.reindexObject()

    pghandler.finish()
