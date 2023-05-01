from django.db import models

class User(models.Model):
    userEmail = models.CharField(primary_key=True, max_length=128)
    userName = models.CharField(max_length=50)
    userImage = models.ImageField(upload_to='userImages/', blank = True, null = True)
    pendingRequests = models.ManyToManyField('Trip', related_name='pending_requests', blank=True)
    acceptedRequests = models.ManyToManyField('Trip', related_name='accepted_requests', blank=True)

class Trip(models.Model):
    owner = models.ForeignKey(User, related_name='trips', on_delete=models.CASCADE)
    tripName = models.CharField(max_length=80)
    tripImage = models.ImageField(upload_to='tripImages/', blank = True, null = True)
    startDate = models.DateField()
    endDate = models.DateField()
    pendingUsers = models.ManyToManyField('User', related_name='pending_users', blank=True)
    sharedUsers = models.ManyToManyField('User', related_name='shared_users', blank=True)

class ItineraryEntry(models.Model):
    trip = models.ForeignKey('Trip', related_name='itinerary_entries', on_delete=models.CASCADE)
    dateTime = models.DateTimeField()
    description = models.CharField(max_length=500)
    location = models.CharField(max_length=80)