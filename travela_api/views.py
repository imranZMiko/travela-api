from django.http import JsonResponse
from rest_framework.decorators import api_view
from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework import status
from .scraper import *
import random


@api_view(['GET', 'POST'])
def users_list(request):
    if request.method == 'GET':
        users = User.objects.all()
        serializer = UserSerializer(users, many = True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = UserSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)

@api_view(['GET', 'PUT', 'DELETE'])
def user_details(request, userID):
    try:
        user = User.objects.get(pk = userID)
    except User.DoesNotExist:
        return Response(status = status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = UserSerializer(user, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        user.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
def user_trips(request, userID):
    try:
        trips = Trip.objects.filter(owner = userID)
    except Trip.DoesNotExist:
        return Response(status = status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = TripSerializer(trips, many = True)
        return Response(serializer.data)
    
    if request.method == 'POST':
        serializer = TripSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)

@api_view(['GET'])
def user_pending_trips(request, userID):
    try:
        trips = Trip.objects.filter(pendingUsers__userEmail__contains = userID)
    except Trip.DoesNotExist:
        return Response(status = status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = TripSerializer(trips, many = True)
        return Response(serializer.data)

@api_view(['GET'])
def user_personal_trips(request, userID):
    try:
        trips = Trip.objects.filter(owner = userID).filter(sharedUsers__isnull=True)
    except Trip.DoesNotExist:
        return Response(status = status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = TripSerializer(trips, many = True)
        return Response(serializer.data)

@api_view(['GET'])
def user_group_trips(request, userID):
    try:
        tripsA = Trip.objects.filter(owner = userID).filter(sharedUsers__isnull=False)
        tripsB = Trip.objects.filter(sharedUsers__userEmail__contains = userID)
        trips = tripsA.union(tripsB)
    except Trip.DoesNotExist:
        return Response(status = status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = TripSerializer(trips, many = True)
        return Response(serializer.data)
        

@api_view(['GET', 'PUT', 'DELETE'])
def trip_details(request, id):
    try:
        trip = Trip.objects.get(pk = id)
    except Trip.DoesNotExist:
        return Response(status = status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = TripSerializer(trip)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = TripSerializer(trip, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        trip.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)
    
@api_view(['GET', 'POST'])
def itinerary_list(request, tripID):  
    if request.method == 'GET':
        try:
            entries = ItineraryEntry.objects.filter(trip = tripID).order_by('dateTime')
        except ItineraryEntry.DoesNotExist:
            return Response(status = status.HTTP_404_NOT_FOUND)
        serializer = ItineraryEntrySerializer(entries, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = ItineraryEntrySerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)

@api_view(['GET', 'PUT', 'DELETE'])
def itinerary_details(request, tripID, id):
    try:
        itinerary = ItineraryEntry.objects.get(pk = id)
    except ItineraryEntry.DoesNotExist:
        return Response(status = status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ItineraryEntrySerializer(itinerary)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = ItineraryEntrySerializer(itinerary, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        itinerary.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def destination_search(request, search_term):
    if request.method == 'GET':
        return Response(getDestinations(search_term))

@api_view(['GET'])
def destination_details(request, search_term):
    if request.method == 'GET':
        return Response(getDestinationDetails(search_term))
    
@api_view(['GET'])
def home_banner(request):
    try:
        destinationSet = HomeDestination.objects.all()
        destination = random.choice(destinationSet)
    except HomeDestination.DoesNotExist:
        return Response(status = status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = DestinationSerializer(destination) 
        return Response(serializer.data)
    
@api_view(['GET'])
def home_hot_destination(request):
    try:
        destinationSet = HomeDestination.objects.all()
        destinations = random.sample(destinationSet, 10)
    except HomeDestination.DoesNotExist:
        return Response(status = status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = [DestinationSerializer(destination) for destination in destinations]
        return Response(serializer.data)

