from django.db import models


class Page(models.Model):
    pass


class Tag(models.Model):
    type = models.TextField(db_index=True)
    value = models.TextField()
    page = models.ForeignKey(Page, on_delete=models.CASCADE)
