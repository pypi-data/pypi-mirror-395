"""Upgrade step to add eea_latest_version block to web_report content type"""

import logging
import uuid
from Products.CMFCore.utils import getToolByName
from Products.ZCatalog.ProgressHandler import ZLogHandler

logger = logging.getLogger("eea.website.policy")


def add_latest_version_block(context):
    """Add eea_latest_version block after page header in web_report.

    Adds the block:
    {
        "@layout": "<generated-uuid>",
        "@type": "eea_latest_version",
        "block": "b06ccfad-8f65-4bcc-a5bd-10647ade323e",
        "results": True
    }
    immediately after the title block in all web_report content.
    """
    ctool = getToolByName(context, "portal_catalog")
    brains = ctool.unrestrictedSearchResults(portal_type="web_report")

    if not brains:
        logger.info("No web_report objects found")
        return

    pghandler = ZLogHandler(100)
    pghandler.init("Add eea_latest_version block to web_report", len(brains))

    modified_count = 0

    for idx, brain in enumerate(brains):
        pghandler.report(idx)

        try:
            doc = brain.getObject()
        except Exception as e:
            logger.warning("Could not get object %s: %s", brain.getPath(), e)
            continue

        # Check if the document has blocks
        if not hasattr(doc, "blocks") or not doc.blocks:
            continue

        # Check if the document has blocks_layout
        if not hasattr(doc, "blocks_layout") or not doc.blocks_layout:
            continue

        # Find the title block (page header)
        title_block_id = None
        for block_id, block_data in doc.blocks.items():
            if isinstance(block_data, dict) and block_data.get("@type") == "title":
                title_block_id = block_id
                break

        if not title_block_id:
            logger.warning("No title block found in %s, skipping", brain.getPath())
            continue

        # Check if eea_latest_version block already exists
        has_latest_version = False
        for block_data in doc.blocks.values():
            if (
                isinstance(block_data, dict)
                and block_data.get("@type") == "eea_latest_version"
            ):
                has_latest_version = True
                break

        if has_latest_version:
            logger.info(
                "eea_latest_version block already exists in %s, skipping",
                brain.getPath(),
            )
            continue

        # Generate a new UUID for this block
        new_block_id = str(uuid.uuid4())

        # The new block to add
        new_block = {
            "@layout": new_block_id,
            "@type": "eea_latest_version",
            "block": "b06ccfad-8f65-4bcc-a5bd-10647ade323e",
            "results": True,
        }

        # Add the new block to blocks
        doc.blocks[new_block_id] = new_block

        # Add to blocks_layout immediately after title block
        if "items" in doc.blocks_layout:
            layout_items = doc.blocks_layout["items"]

            if title_block_id in layout_items:
                title_index = layout_items.index(title_block_id)
                # Insert after the title block
                layout_items.insert(title_index + 1, new_block_id)
                modified_count += 1
                logger.info("Added eea_latest_version block to %s", brain.getPath())
            else:
                logger.warning(
                    "Title block %s not found in blocks_layout for %s",
                    title_block_id,
                    brain.getPath(),
                )
                # Remove the block we just added since we can't
                # place it correctly
                del doc.blocks[new_block_id]
                continue

        # Mark object as modified
        doc._p_changed = True
        doc.reindexObject()

    pghandler.finish()
    logger.info(
        "Successfully added eea_latest_version block to %s web_report objects",
        modified_count,
    )
