from django.db import models

class User(models.Model):
    email = models.EmailField(max_length=50)
    usrname = models.CharField(max_length=50)

class Post(models.Model):
    # id
    date = models.DateTimeField('date posted')
    subject = models.CharField(max_length=50)
    body = models.CharField(max_length=200)

# Create your models here.
