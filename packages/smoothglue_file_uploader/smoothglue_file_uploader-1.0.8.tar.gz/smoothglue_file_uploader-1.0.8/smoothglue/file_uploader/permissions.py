from abc import ABC, abstractmethod


class BaseDocumentPermission(ABC):
    @abstractmethod
    def has_permission(self, request, view, document) -> bool:
        raise NotImplementedError


class DefaultDocumentPermission(BaseDocumentPermission):
    def has_permission(self, request, view, document) -> bool:
        return True
