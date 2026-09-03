from django.db import models


# Create your models here.

class Publisher(models.Model):
    '''Model representing a publisher.'''
    name = models.CharField(max_length=100)

    def title(self):
        return self.id

    def __str__(self):
        return self.name
