from abc import abstractmethod
from mjxml.asset import Asset
from mjxml.commons import MJCElement

# This exists solely to prevent a circular import

__all__ = ["BodyChildren"]


class BodyChildren(MJCElement):
    @abstractmethod
    def remove_duplicate_assets(self, existing: dict[int, Asset]) -> None:
        pass