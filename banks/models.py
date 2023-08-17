from django.db import models
from django.contrib.auth.models import User


class Bank(models.Model):
    name      = models.CharField(max_length=200)
    swift_code = models.CharField(max_length=200)
    inst_num = models.CharField(max_length=200)
    description     = models.CharField(max_length=200)
    owner    = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    


class Branch(models.Model):
    name      = models.CharField(max_length=200)
    transit_num = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    email       = models.EmailField(default='admin@utoronto.ca')
    capacity = models.PositiveIntegerField(null=True)
    last_modified       = models.DateField(auto_now=True, auto_now_add=False)
    bank = models.ForeignKey('Bank', on_delete=models.SET_NULL, null=True)

