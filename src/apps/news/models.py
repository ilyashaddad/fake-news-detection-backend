from djongo import models

# Create your models here.
class News(models.Model):
    name = models.TextField()