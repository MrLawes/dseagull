from django.db import models

from dseagull.models import BaseModel


class Person(BaseModel):
    first_name = models.CharField(max_length=30, default='')
    last_name = models.CharField(max_length=30, default='')
