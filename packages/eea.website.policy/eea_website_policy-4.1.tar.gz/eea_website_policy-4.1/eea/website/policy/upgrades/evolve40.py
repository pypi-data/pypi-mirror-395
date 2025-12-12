"""Upgrade to version 2.0"""

import logging
from plone import api
from zope.component import queryMultiAdapter

logger = logging.getLogger("eea.website.policy")


def migrate_teaser(context):
    """Fix Indicator schema"""
    portal = api.portal.get()
    view = queryMultiAdapter((portal, context.REQUEST), name="teaser-migrate")
    count = view.migrate()
    logger.info("Migrated %s objects Teaser Blocks", count)
    view = queryMultiAdapter((portal, context.REQUEST), name="teaser-layout-migrate")
    count = view.migrate()
    logger.info("Migrated %s c-types layouts: teaserGrid to gridBlock", count)
