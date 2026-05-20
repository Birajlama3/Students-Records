from django.db import models

class User(models.Model):
    age = models.TextField()
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name