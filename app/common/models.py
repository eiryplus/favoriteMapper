from django.db import models


class ModelBase(models.Model):
    created_at = models.DateTimeField(verbose_name="登録日", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="登録日", auto_now=True)

    class Meta:
        abstract = True
