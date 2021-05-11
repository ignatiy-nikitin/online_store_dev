from django.db import models


class File(models.Model):
    name = models.CharField(max_length=128)
    # дата добавления

    def __str__(self):
        return self.name