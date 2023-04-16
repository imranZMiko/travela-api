from rest_framework import serializers
from .models import *

class ItineraryEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = ItineraryEntry
        fields = ['trip', 'dateTime', 'description', 'location']

class TripSerializer(serializers.ModelSerializer):
    itinerary_entries = ItineraryEntrySerializer(many=True, read_only=True)

    class Meta:
        model = Trip
        fields = ['owner', 'tripName', 'tripImage', 'startDate', 'endDate', 'sharedUsers', 'itinerary_entries']

class UserSerializer(serializers.ModelSerializer):
    trips = TripSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['userID', 'userName', 'userImage', 'trips']