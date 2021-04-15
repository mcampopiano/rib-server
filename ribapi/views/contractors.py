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

        return Response(serializer.data)


class ContractorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contractor
        fields = ('name',)
