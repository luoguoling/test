from django.db import models

# Create your models here.
class serverlist(models.Model):
    agent = models.CharField(max_length=100)
    serverId = models.IntegerField()
    ipaddress = models.IPAddressField()
