from django.db import models
from rest_framework.authtoken.models import Token

class Contractor(models.Model):
    user = models.ForeignKey(Token, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)