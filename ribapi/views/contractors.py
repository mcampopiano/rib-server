from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework import viewsets
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rest_framework.authtoken.models import Token
from ribapi.models import Contractor

class Contractors(ViewSet):

    def list(self, request):
        contractors = Contractor.objects.all()

        serializer = ContractorSerializer(contractors, many=True, context={'request': request})

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def create(self, request):
        contractor = Contractor()
        contractor.name = request.data['name']

        contractor.save()
        serializer = ContractorSerializer(contractor, many=False, context={'request': request})

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, pk=None):
        contractor = Contractor()
        contractor.name = request.data['name']

        contractor.save()
        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def retrieve(self, request, pk=None):
        contractor = Contractor.objects.get(pk=pk)

        serializer = ContractorSerializerWithClients(contractor, many=False, context={'request': request})

        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        contractor = Contractor.objects.get(pk=pk)
        contractor.delete()

        return Response({}, status=status.HTTP_204_NO_CONTENT)


class ContractorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contractor
        fields = ('id', 'name')

class ContractorSerializerWithClients(serializers.ModelSerializer):
    class Meta:
        model = Contractor
        fields = ('id', 'name', 'clients')
        depth = 1