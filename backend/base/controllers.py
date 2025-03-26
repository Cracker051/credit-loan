from typing import List, override

from rest_framework.permissions import BasePermission
from rest_framework.request import HttpRequest
from rest_framework.response import Response
from rest_framework.serializers import BaseSerializer
from rest_framework.views import APIView

from backend.base.services import BaseService


class BaseAPIController(APIView):
    permission_classes: dict[str, BasePermission] = dict()
    serializer_classes: dict[str, BaseSerializer] = dict()
    service_classes: dict[str, BaseService] = dict()

    @classmethod
    def get_serializer(cls, request: HttpRequest) -> BaseSerializer:
        serializer_cls = cls.serializer_classes.get(request.method.lower()) or cls.serializer_classes.get("default")
        if serializer_cls is None:
            raise KeyError("You must implement default `serializer` if else is empty")
        return serializer_cls(data=request.data)

    @override
    def get_permissions(self) -> List[BasePermission]:
        endpoint_permissions = self.permission_classes.get(self.request.method.upper(), [])
        mixed_permissions = set(endpoint_permissions + super().permission_classes)  # to prevent duplicates
        return [permission() for permission in mixed_permissions]

    def get_service(self, request: HttpRequest):
        service_cls = self.service_classes.get(request.method.lower(), self.http_method_not_allowed)
        return service_cls

    @override
    def dispatch(self, request: HttpRequest, *args, **kwargs) -> Response:
        self.args = args
        self.kwargs = kwargs
        request = self.initialize_request(request, *args, **kwargs)
        self.request = request
        self.headers = self.default_response_headers

        self.initial(request, *args, **kwargs)
        try:
            if request.method.lower() not in self.service_classes.keys():
                raise self.http_method_not_allowed(request)

            service_cls = self.get_service(request)

            serializer = self.get_serializer(request)

            serializer.is_valid(raise_exception=True)
            service = service_cls(**serializer.validated_data)
            response = service.response
        except Exception as exc:
            response = self.handle_exception(exc)

        self.response = self.finalize_response(request, response, *args, **kwargs)
        return self.response
