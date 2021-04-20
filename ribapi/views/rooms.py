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
        cf = sq * request.data['height']
        air_movers = 1

        room.name = request.data['name']
        room.width = request.data['width']
        room.length = request.data['length']
        room.height = request.data['height']
        room.ceiling_damage = request.data['ceilingDamage']
        room.damage_above_two_feet = request.data['damageAboveTwoFeet']
        room.air_movers_min = air_movers + math.ceil(sq/70)
        room.air_movers_max = air_movers + math.ceil(sq/50)

        # Use if damage above two feet on the walls
        if room.damage_above_two_feet and len(request.data['walls']) > 0:
            sq_walls = 0
            for wall in request.data['walls']:
                height = wall['height'] - 2
                sq_walls = sq_walls + (height * wall['length'])
            room.air_movers_min = room.air_movers_min + math.ceil(sq_walls/150)
            room.air_movers_max = room.air_movers_max + math.ceil(sq_walls/100)

        # Use if ceiling damage
        if room.ceiling_damage:
            room.air_movers_min = room.air_movers_min + math.ceil(sq/150)
            room.air_movers_max = room.air_movers_max + math.ceil(sq/100)
        

        room.dehumidifier_min_size = None
        room.dehumidifier_max_size = None
        # room.save()

        serializer = RoomSerializer(room, many=False, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model=Room
        fields=('name', 'width', 'height', 'length', 'air_movers_min', 'air_movers_max', 'dehumidifier_min_size',
        'dehumidifier_max_size', 'ceiling_damage', 'damage_above_two_feet')