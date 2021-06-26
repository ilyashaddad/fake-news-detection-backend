from djongo import models
 
class User(models.Model):
    name = models.TextField()