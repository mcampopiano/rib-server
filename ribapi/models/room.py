from django.db import models

class Room(models.Model):
    client = models.ForeignKey("Client", on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    air_movers_min = models.IntegerField()
    air_movers_max = models.IntegerField()
    dehumidifier_min_size = models.CharField(max_length=50)
    dehumidifier_max_size = models.CharField(max_length=50)
    width = models.IntegerField()
    height = models.IntegerField()
    length = models.IntegerField()
    ceiling_damage = models.BooleanField()
    damage_above_two_feet = models.BooleanField()