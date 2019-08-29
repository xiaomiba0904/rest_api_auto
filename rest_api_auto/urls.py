from django.urls import path

from rest_api_auto.views import ListCreateApiView, GetUpdateApiView


urlpatterns = [
    path('<str:app>/<str:model>/', ListCreateApiView()),
    path('<str:app>/<str:model>/<slug:pk>/', GetUpdateApiView()),

]