from django.db import models

# Create your models here.

class Product(models.Model):
    title = models.CharField(max_length=200)
    image = models.CharField(max_length=20)
    likes = models.PositiveIntegerField(default=0)
    comment = models.CharField(max_length=200)


class User(models.Model):
    pass

