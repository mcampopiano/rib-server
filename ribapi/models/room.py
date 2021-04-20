from django.db import models

class Room(models.Model):
    client = models.ForeignKey("Client", on_delete=models.CASCADE, related_name='rooms')
    name = models.CharField(max_length=50)
    air_movers_min = models.IntegerField()
    air_movers_max = models.IntegerField()
    dehumidifier_size = models.CharField(max_length=50)
    width = models.FloatField()
    height = models.FloatField()
    length = models.FloatField()
    ceiling_damage = models.BooleanField()
    damage_above_two_feet = models.BooleanField()