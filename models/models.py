from django.db import models


# Create your models here.
class News(models.Model):
    title = models.CharField(max_length=200)
    url = models.CharField(max_length=200)
    source = models.CharField(max_length=200)
    update = models.DateField()
    newchoices = (
        (0, "old"),
        (1, "new"),
    )
    new = models.SmallIntegerField(choices=newchoices)


class Publications(models.Model):
    title = models.CharField(max_length=200)
    url = models.CharField(max_length=200)
    source = models.CharField(max_length=200)
    update = models.DateField()
    newchoices = (
        (0, "old"),
        (1, "new"),
    )
    new = models.SmallIntegerField(choices=newchoices)


class Updates(models.Model):
    title = models.CharField(max_length=200)
    note = models.CharField(max_length=200)
    update = models.DateField()
    newchoices = (
        (0, "old"),
        (1, "new"),
    )
    new = models.SmallIntegerField(choices=newchoices)

