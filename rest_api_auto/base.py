from collections import OrderedDict

from django.http import JsonResponse
from rest_framework.generics import CreateAPIView, UpdateAPIView, DestroyAPIView, ListAPIView, RetrieveAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer

from rest_api_auto import CRUD


class DefaultPagination(PageNumberPagination):

    def get_paginated_response(self, data):
        return self.get_json_response(data)

    def get_default_response(self, data):
        return Response(self.get_response_data(data))

    def get_json_response(self, data):
        return JsonResponse(self.get_response_data(data))

    def get_response_data(self, data):
        return OrderedDict([
            ('code', 200),
            ('count', self.page.paginator.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data)
        ])


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
        self.view_classes = dict()
        for a in self.actions:
            if a not in self.ACTIONS_VIEW:
                raise ValueError(f"不支持生成 {a} 操作")
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
        queryset = self.get_default_queryset()
        serializer_class = self.create_default_serializer()

        for a in self.actions:
            for base_view in self.ACTIONS_VIEW[a]:
                model_view_class = type(
                    self.name + base_view.__name__, (base_view, ),
                    {
                        "queryset": queryset,
                        "pagination_class": DefaultPagination,
                        "serializer_class": serializer_class
                    }
                )
                self.view_classes[base_view] = model_view_class
