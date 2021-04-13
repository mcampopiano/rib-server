from django.db import models
from rest_framework.authtoken.models import Token

class Client(models.Model):
    user = models.ForeignKey(Token, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    claim_number = models.CharField(max_length=500)
    contractor = models.ForeignKey("contractor", on_delete=models.CASCADE)