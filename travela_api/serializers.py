from rest_framework import serializers
from .models import *

#Serializer for itinerary entry
class ItineraryEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = ItineraryEntry
        #Fields required for itinerary entry
        fields = ['id', 'trip', 'dateTime', 'description', 'location_latitude', 'location_longitude']

#Serializer for trip
class TripSerializer(serializers.ModelSerializer):
    itinerary_entries = ItineraryEntrySerializer(many=True, read_only=True)

    class Meta:
        model = Trip
        #Fields required for trip
        fields = ['id', 'owner', 'tripName', 'tripImage', 'startDate', 'endDate', 'pendingUsers', 'sharedUsers', 'itinerary_entries']

#Serializer for user
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        #Fields required for user
        fields = ['userEmail', 'userName', 'userImage']

#Serializer for destination
class DestinationSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomeDestination
        #Fields required for destination
        fields = ['destinationName', 'destinationTag', 'destinationImage', 'destinationLocation']