from django.db import models


class BaseModel(models.Model):
    class Meta:
        abstract = True

    created = models.DateTimeField(
        auto_now_add=True, verbose_name='创建时间', db_index=True,
    )
    updated = models.DateTimeField(
        auto_now=True, verbose_name='更新时间', db_index=True,
    )
