from collections import OrderedDict

from rest_framework.generics import CreateAPIView, UpdateAPIView, DestroyAPIView, ListAPIView, RetrieveAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer

from rest_api_auto import CRUD


class DefaultPagination(PageNumberPagination):
    page_size = 10

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('code', 200),
            ('count', self.page.paginator.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data)
        ]))


class APIManager(object):
    """
    api 管理类
    """
    ACTIONS_VIEW = {
        "C": (CreateAPIView,),
        "R": (ListAPIView, RetrieveAPIView),
        "U": (UpdateAPIView, ),
        "D": (DestroyAPIView, )
    }

    def __init__(self, name, model, actions=CRUD):
        self.name = name
        self.model = model
        self.actions = actions
        self.create_default_view()

    def get_default_queryset(self):
        return self.model.objects.all().order_by("-pk")

    def create_default_serializer(self):
        class Meta:
            model = self.model
            fields = '__all__'

        return type(
            self.name + "Serializer",
            (ModelSerializer, ),
            {"Meta": Meta}
        )

    def create_default_view(self):
        """
        创建对应的处理类
        """
        self._view_classes = set()
        queryset = self.get_default_queryset()
        serializer_class = self.create_default_serializer()

        for a in self.actions:
            if a not in self.ACTIONS_VIEW:
                continue

            for view in self.ACTIONS_VIEW[a]:
                view_class = type(
                    self.name + view.__name__, (view, ),
                    {
                        "queryset": queryset,
                        "pagination_class": DefaultPagination,
                        "serializer_class": serializer_class
                    }
                )
                setattr(self, view_class.__name__.lower(), view_class)
                self._view_classes.add(view_class)
