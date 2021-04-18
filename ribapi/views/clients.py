from django.core.exceptions import ValidationError
from django.http.response import HttpResponse
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework import viewsets
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rest_framework.authtoken.models import Token
from ribapi import models
from ribapi.models import Client, Contractor

class Clients(ViewSet):
    def list(self, request):
        user = Token.objects.get(user = request.auth.user)
        clients = Client.objects.filter(user=user)

    
        serializer = ClientSerializer(clients, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        user = Token.objects.get(user = request.auth.user)
        contractor = Contractor.objects.get(pk = request.data['contractorId'])
        client = Client()
        client.name = request.data['name']
        client.claim_number = request.data['claimNumber']
        client.user = user
        client.contractor = contractor
        client.save()
        
        serializer = ClientSerializer(client, many=False, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)


    
class ContractorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contractor
        fields = ('name',)

class ClientSerializer(serializers.ModelSerializer):
    contractor = ContractorSerializer()
    class Meta:
        model = Client
        fields = ('name', 'claim_number', 'contractor')