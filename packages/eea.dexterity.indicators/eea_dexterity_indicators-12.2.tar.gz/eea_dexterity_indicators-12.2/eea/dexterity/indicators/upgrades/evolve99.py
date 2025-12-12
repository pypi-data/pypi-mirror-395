""" Upgrade to 9.9 """
from Products.CMFCore.utils import getToolByName
from Products.ZCatalog.ProgressHandler import ZLogHandler


def to_99(context):
    """ Upgrade to 9.9 """
    ctool = getToolByName(context, "portal_catalog")
    brains = ctool.unrestrictedSearchResults(portal_type="ims_indicator")
    pghandler = ZLogHandler(100)
    pghandler.init("Reindex IMS indicator SearchableText", len(brains))
    for idx, brain in enumerate(brains):
        pghandler.report(idx)
        indicator = brain.getObject()
        indicator.reindexObject(idxs=['SearchableText'])
    pghandler.finish()
