from django.urls import path

from rest_api_auto.views import list_or_create_view, get_or_update_view


urlpatterns = [
    path('<str: app>/<str: model>/', list_or_create_view),
    path('<str: app>/<str: model>/<slug: pk>/', get_or_update_view),
]