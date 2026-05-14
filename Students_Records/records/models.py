from django.db import models

class Records(models.Model):
    name = models.CharField( max_length=50)
    stack = models.CharField(max_length=50)
    title = models.CharField(max_length=50)
    description = models.TextField( max_length =250)
    date = models.DateField()
    hours_worked = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)


