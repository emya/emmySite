from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Purchase(models.Model):
    user = models.ForeignKey(User)
    price = models.IntegerField()
    date = models.DateTimeField('data purchased')
    menu = models.IntegerField()

