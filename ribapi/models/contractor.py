from django.db import models
from rest_framework.authtoken.models import Token

class Contractor(models.Model):
    name = models.CharField(max_length=50)