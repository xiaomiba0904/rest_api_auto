from django.http import HttpResponseNotFound
from rest_framework import exceptions
from rest_framework.generics import CreateAPIView, UpdateAPIView, DestroyAPIView, ListAPIView, RetrieveAPIView

from rest_api_auto import _api_globals
from rest_api_auto.utils import url_parameter_conversion


class DispatchView(object):

    _route = {}

    def __call__(self, request, *args, **kwargs):
        name, _ = url_parameter_conversion(**kwargs)

        if name not in _api_globals:
            return HttpResponseNotFound()

        self.manager = _api_globals[name]

        if request.method not in self._route.keys():
            raise exceptions.MethodNotAllowed(request.method)

        view_class = self.dispatch(request)
        return view_class.as_view()(request, *args, **kwargs)

    def dispatch(self, request):
        view_class = self._route.get(request.method)
        if not view_class:
            raise exceptions.MethodNotAllowed(request.method)
        return view_class


class ListCreateApiView(DispatchView):

    _route = {
        "GET": ListAPIView,
        "POST": CreateAPIView
    }


class GetUpdateApiView(DispatchView):

    _route = {
        "GET": RetrieveAPIView,
        "PUT": UpdateAPIView,
        "PATCH": UpdateAPIView,
        "DELETE": DestroyAPIView
    }
