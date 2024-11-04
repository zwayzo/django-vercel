from django.db import models
from django import forms
# Create your models here.


class Room(models.Model):
    #host
    #topic
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    #participants
    updates = models.DateTimeField(auto_now=True)
    create = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    

class User(models.Model):
    name = models.CharField(max_length=50, primary_key=True)
    email = models.EmailField(max_length=254, blank=True)
    password = models.CharField(max_length=50)

    class Meta:
        db_table = 'table1'  # Specify the name of the table if it doesn't follow Django's naming conventions
        managed = False  # This tells Django not to manage the table (no migrations, etc.)
        
    def __str__(self):
        return self.name
