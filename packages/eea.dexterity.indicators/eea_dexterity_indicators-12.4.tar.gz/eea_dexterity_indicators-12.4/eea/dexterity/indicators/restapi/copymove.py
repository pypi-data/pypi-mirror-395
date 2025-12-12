"""Custom @copy / @move RestAPI endpoints"""

from plone.restapi.services.copymove.copymove import Copy as BaseCopy
from plone.restapi.services.copymove.copymove import Move as BaseMove


class Copy(BaseCopy):
    """Copies existing content objects."""

    def get_object(self, key):
        """Get object by key"""
        obj = super().get_object(key)
        if obj:
            return obj

        key = key.strip("/")
        return self.context.restrictedTraverse(key, None)


class Move(BaseMove):
    """Moves existing content objects."""

    def get_object(self, key):
        """Get object by key"""
        obj = super().get_object(key)
        if obj:
            return obj

        key = key.strip("/")
        return self.context.restrictedTraverse(key, None)
