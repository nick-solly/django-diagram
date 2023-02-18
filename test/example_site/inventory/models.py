from django.db import models


class Location(models.Model):
    item = models.OneToOneField("core.item", on_delete=models.CASCADE)
    shelf = models.CharField(max_length=100)

    def __str__(self):
        return str(self.id)
