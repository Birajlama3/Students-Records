from django.db import models

class Records(models.Mmodel):
    name = models.CharField( max_length=50)
    task = models.CharField()
