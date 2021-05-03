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
    
    def destroy(self, request, pk=None):
        room = Room.objects.get(pk=pk)
        room.delete()
        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def create(self, request):
        room = Room()
        client = Client.objects.get(pk=request.data['clientId'])
        sq = request.data['length'] * request.data['width']
        cf = sq * request.data['height']
        air_movers = 1
        PPD = 0

        room.client = client
        room.name = request.data['name']
        room.width = request.data['width']
        room.length = request.data['length']
        room.height = request.data['height']
        room.ceiling_damage = request.data['ceilingDamage']
        room.damage_above_two_feet = request.data['damageAboveTwoFeet']
        room.air_movers_min = air_movers + math.ceil(sq/70)
        room.air_movers_max = air_movers + math.ceil(sq/50)

        # Calculate size of dehumidifier
        if request.data['class'] == 1:
            PPD = cf / 100
        elif request.data['class'] == 2:
            PPD = cf / 50
        elif request.data['class'] == 3 or request.data['class'] == 4:
            PPD = cf / 40
        
        if PPD <= 69:
            room.dehumidifier_size = "Standard"
        elif PPD in range(70, 109):
            room.dehumidifier_size = "Large"
        elif PPD in range(110, 159):
            room.dehumidifier_size = "XLarge"
        else:
            room.dehumidifier_size = "XXLarge"

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
        room.save()

        serializer = RoomSerializer(room, many=False, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        room = Room.objects.get(pk=pk)
        client = room.client
        sq = request.data['length'] * request.data['width']
        cf = sq * request.data['height']
        air_movers = 1
        PPD = 0

        room.client = client
        room.name = request.data['name']
        room.width = request.data['width']
        room.length = request.data['length']
        room.height = request.data['height']
        room.ceiling_damage = request.data['ceilingDamage']
        room.damage_above_two_feet = request.data['damageAboveTwoFeet']
        room.air_movers_min = air_movers + math.ceil(sq/70)
        room.air_movers_max = air_movers + math.ceil(sq/50)

        # Calculate size of dehumidifier
        if request.data['class'] == 1:
            PPD = cf / 100
        elif request.data['class'] == 2:
            PPD = cf / 50
        elif request.data['class'] == 3 or request.data['class'] == 4:
            PPD = cf / 40
        
        if PPD <= 69:
            room.dehumidifier_size = "Standard"
        elif PPD in range(70, 109):
            room.dehumidifier_size = "Large"
        elif PPD in range(110, 159):
            room.dehumidifier_size = "XLarge"
        else:
            room.dehumidifier_size = "XXLarge"

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
        room.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)



class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model=Room
        fields=('id', 'name', 'width', 'height', 'length', 'air_movers_min', 'air_movers_max', 'dehumidifier_size', 'ceiling_damage', 'damage_above_two_feet')