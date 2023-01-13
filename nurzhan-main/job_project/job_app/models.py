from django.db import models

class JobInformation(models.Model):
    name = models.CharField(max_length=255)
    salary = models.IntegerField()
    year = models.CharField(max_length=4)
    skills = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
