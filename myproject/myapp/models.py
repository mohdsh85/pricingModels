from django.db import models

# Create your models here.

class Dreamreal(models.Model):

   website = models.CharField(max_length = 50)
   mail = models.CharField(max_length = 50)
   name = models.CharField(max_length = 50)
   phonenumber = models.IntegerField()
   last_name=models.CharField(max_length=50)

   class Meta:
      db_table = "dreamreal"