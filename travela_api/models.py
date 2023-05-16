from django.db import models
from django.utils import timezone

#Model for user
class User(models.Model):
    #Fields required for the user
    userEmail = models.CharField(primary_key=True, max_length=128)
    userName = models.CharField(max_length=50)
    userImage = models.ImageField(upload_to='userImages/', blank = True, null = True)

#Model for trip
class Trip(models.Model):
    #Fields required for trip
    owner = models.ForeignKey(User, related_name='trips', on_delete=models.CASCADE)
    tripName = models.CharField(max_length=80)
    tripImage = models.ImageField(upload_to='tripImages/', blank = True, null = True)
    startDate = models.DateField()
    endDate = models.DateField()
    pendingUsers = models.ManyToManyField('User', related_name='pending_users', blank=True)
    sharedUsers = models.ManyToManyField('User', related_name='shared_users', blank=True)

#Model for itinerary entry
class ItineraryEntry(models.Model):
    #Fields required for itinerary entry
    trip = models.ForeignKey('Trip', related_name='itinerary_entries', on_delete=models.CASCADE)
    dateTime = models.CharField(max_length=80)
    description = models.CharField(max_length=800)
    location_latitude = models.DecimalField(max_digits=25, decimal_places=20)
    location_longitude = models.DecimalField(max_digits=25, decimal_places=20)

#Model for home destination
class HomeDestination(models.Model):
    #Fields required for home destination
    destinationName = models.CharField(max_length=50)
    destinationTag = models.CharField(max_length=50)
    destinationImage = models.CharField(max_length=200)
    destinationLocation = models.CharField(max_length=50)
    