from djongo import models


class Comment(models.Model):
    name = models.TextField()