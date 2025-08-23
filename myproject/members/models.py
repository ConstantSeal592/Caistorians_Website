from django.db import models

class member(models.Model):
    firstname = models.CharField(max_length=20)
    surname = models.CharField(max_length=20)
    left_caistor = models.IntegerField()
    statement = models.CharField(max_length=4095)