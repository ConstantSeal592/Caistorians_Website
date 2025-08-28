from django.db import models

class member(models.Model):
    firstname = models.CharField(max_length=20)
    surname = models.CharField(max_length=20)
    year_left = models.IntegerField()
    statement = models.CharField(max_length=4095)
    static_img_path = models.CharField(max_length=255,null="")

    def __str__(self):
        return f"{self.firstname} {self.surname}"