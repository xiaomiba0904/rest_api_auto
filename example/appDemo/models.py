from django.db import models
from rest_api_auto.decorators import register_model
# Create your models here.


@register_model()
class MoDemo(models.Model):

    name = models.CharField(max_length=16)
    age = models.IntegerField()
    address = models.CharField(max_length=256)
    is_admin = models.BooleanField(default=False)
