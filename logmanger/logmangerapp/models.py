from django.db import models

# Create your models here.
class AddLogpath(models.Model):
	logpath = models.CharField(max_length=500)
        logtype = models.CharField(max_length=50)
class AddPhpLogpath(models.Model):
    logpath = models.CharField(max_length=500)
