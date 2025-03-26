from abc import ABC, abstractmethod

from rest_framework.response import Response

from backend.authorize.models import User


class BaseService(ABC):
    def __init__(self, user: User | None = None, **kwargs) -> None:
        self.user = user
        self.kwargs = kwargs

    @property
    @abstractmethod
    def response(self) -> Response:
        pass
