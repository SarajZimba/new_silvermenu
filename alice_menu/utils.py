from django.db import models


class Manger(models.Manager):
    def is_not_deleted(self):
        return self.filter(is_deleted=False)

    def active(self):
        return self.filter(is_deleted=False, status=True)


class BaseModel(models.Model):
    """
    This is the base model for all the models.
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    sorting_order = models.IntegerField(default=0)
    is_featured = models.BooleanField(default=False)
    objects = Manger()

    class Meta:
        abstract = True
        ordering = ["-created_at"]