from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework import viewsets
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rest_framework.authtoken.models import Token
from ribapi import models
from ribapi.models import Client

class Clients(ViewSet):
    def list(self, request):
        clients = Client.objects.all()

    
        serializer = ClientSerializer(clients, many=True, context={'request': request})
        return Response(serializer.data)
    

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ('name', 'claim_number', 'contractor')