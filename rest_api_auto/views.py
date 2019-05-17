from django.http import HttpResponseNotFound

from rest_api_auto import _api_globals
from rest_api_auto.utils import url_parameter_conversion


class DispatchView(object):

    def __call__(self, request, *args, **kwargs):
        name, _ = url_parameter_conversion(**kwargs)

        if name not in _api_globals:
            return HttpResponseNotFound()

        self.manager = _api_globals[name]



def list_or_create_view(request, *args, **kwargs):
    pass



def get_or_update_view(request, *args, **kwargs):
    pass