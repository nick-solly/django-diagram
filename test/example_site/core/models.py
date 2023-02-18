from django.db import models


class ItemType(models.Model):
    name = models.CharField(max_length=100)

    def __int__(self):
        return self.name


class Item(models.Model):
    name = models.CharField(max_length=100)
    item_types = models.ManyToManyField(ItemType)
    weight = models.IntegerField()

    def __int__(self):
        return self.name


class Buyer(models.Model):
    name = models.CharField(max_length=100)

    def __int__(self):
        return self.name


class Purchase(models.Model):
    item = models.OneToOneField(Item, on_delete=models.CASCADE)
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE)
    price = models.IntegerField()

    def __int__(self):
        return str(self.id)
