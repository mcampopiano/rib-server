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
from ribapi.models import Room, Client

class Rooms(ViewSet):
    def list(self, request):
        rooms = Room.objects.all()

        serializer = RoomSerializer(rooms, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model=Room
        fields=('name', 'width', 'height', 'length', 'air_movers_min', 'air_movers_max', 'dehumidifier_min_size',
        'dehumidifier_max_size', 'ceiling_damage', 'damage_above_two_feet')