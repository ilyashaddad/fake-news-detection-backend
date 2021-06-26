from djongo import models

# Create your models here.
class News_s(models.Model):
    title = models.CharField(max_length=1000)
    image = models.ImageField()
    date = models.DateField(auto_now=True)
    resume = models.TextField()
    thematic = models.CharField(max_length=100)
    description = models.TextField()
    fake_flag = models.CharField(max_length=10)

class Nlp(models.Model):
    title = models.CharField(max_length=1000)
    method =models.CharField(max_length=1000)
    result = models.CharField(max_length=1000)