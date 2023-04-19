from django.db import models

class User(models.Model):
    userID = models.CharField(primary_key=True, max_length=128)
    userName = models.CharField(max_length=50)
    userImage = models.ImageField(upload_to='userImages/', blank = True, null = True)

class Trip(models.Model):
    owner = models.ForeignKey(User, related_name='trips', on_delete=models.CASCADE)
    tripName = models.CharField(max_length=80)
    tripImage = models.ImageField(upload_to='tripImages/')
    startDate = models.DateField()
    endDate = models.DateField()
    sharedUsers = models.ManyToManyField(User, blank=True)

class ItineraryEntry(models.Model):
    trip = models.ForeignKey(Trip, related_name='itinerary_entries', on_delete=models.CASCADE)
    dateTime = models.DateTimeField()
    description = models.CharField(max_length=500)
    location = models.CharField(max_length=80)