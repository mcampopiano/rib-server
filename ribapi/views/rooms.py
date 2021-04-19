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
import math

class Rooms(ViewSet):
    def list(self, request):
        rooms = Room.objects.all()

        serializer = RoomSerializer(rooms, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        room = Room()
        sq = request.data['length'] * request.data['width']
        air_movers = 1

        room.name = request.data['name']
        room.width = request.data['width']
        room.length = request.data['length']
        room.air_movers_min = air_movers + math.ceil(sq/70)
        room.air_movers_max = air_movers + math.ceil(sq/50)

        room.dehumidifier_min_size = None
        room.dehumidifier_max_size = None
        room.ceiling_damage = False
        room.damage_above_two_feet = False

        serializer = RoomSerializer(room, many=False, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model=Room
        fields=('name', 'width', 'height', 'length', 'air_movers_min', 'air_movers_max', 'dehumidifier_min_size',
        'dehumidifier_max_size', 'ceiling_damage', 'damage_above_two_feet')