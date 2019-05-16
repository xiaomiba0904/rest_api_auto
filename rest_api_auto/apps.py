from django.apps import AppConfig


class RestApiAutoConfig(AppConfig):
    name = 'rest_api_auto'
    verbose_name = "Django REST API Auto"

    def ready(self):
        pass