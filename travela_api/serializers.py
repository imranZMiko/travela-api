from rest_framework import serializers
from .models import *

class ItineraryEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = ItineraryEntry
        fields = ['id', 'trip', 'dateTime', 'description', 'location_latitude', 'location_longitude']

class TripSerializer(serializers.ModelSerializer):
    itinerary_entries = ItineraryEntrySerializer(many=True, read_only=True)

    class Meta:
        model = Trip
        fields = ['id', 'owner', 'tripName', 'tripImage', 'startDate', 'endDate', 'pendingUsers', 'sharedUsers', 'itinerary_entries']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['userEmail', 'userName', 'userImage']

class DestinationSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomeDestination
        fields = ['destinationName', 'destinationTag', 'destinationImage', 'destinationLocation']