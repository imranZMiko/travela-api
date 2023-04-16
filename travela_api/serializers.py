from rest_framework import serializers
from .models import *

class ItineraryEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = ItineraryEntry
        fields = ['id', 'trip', 'dateTime', 'description', 'location']

class TripSerializer(serializers.ModelSerializer):
    itinerary_entries = ItineraryEntrySerializer(many=True, read_only=True)

    class Meta:
        model = Trip
        fields = ['id', 'owner', 'tripName', 'tripImage', 'startDate', 'endDate', 'sharedUsers', 'itinerary_entries']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['userID', 'userName', 'userImage']