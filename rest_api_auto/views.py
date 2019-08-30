from django.http import HttpResponseNotFound
from rest_framework import exceptions
from rest_framework.generics import CreateAPIView, UpdateAPIView, DestroyAPIView, ListAPIView, RetrieveAPIView

from rest_api_auto import _api_globals
from rest_api_auto.utils import url_parameter_conversion


class BaseView(object):

    csrf_exempt = True
    _route = {}

    def __call__(self, request, *args, **kwargs):
        name, _ = url_parameter_conversion(**kwargs)

        if name not in _api_globals:
            return HttpResponseNotFound()

        self.manager = _api_globals[name]

        if request.method not in self._route.keys():
            raise exceptions.MethodNotAllowed(request.method)

        base_class = self.dispatch(request)
        if base_class in self.manager.view_classes:
            view_class = self.manager.view_classes[base_class]
        else:
            view_class = base_class

        return view_class.as_view()(request, *args, **kwargs)

    def dispatch(self, request):
        view_class = self._route.get(request.method)
        if not view_class:
            raise exceptions.MethodNotAllowed(request.method)
        return view_class


class ListCreateApiView(BaseView):

    _route = {
        "GET": ListAPIView,
        "POST": CreateAPIView
    }


class GetUpdateApiView(BaseView):

    _route = {
        "GET": RetrieveAPIView,
        "PUT": UpdateAPIView,
        "PATCH": UpdateAPIView,
        "DELETE": DestroyAPIView
    }
