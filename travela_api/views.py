from django.http import JsonResponse
from rest_framework.decorators import api_view
from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework import status


@api_view(['POST'])
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
        

@api_view(['GET', 'PUT', 'DELETE'])
def trip_details(request, userID, id):
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
def itinerary_list(request, userID, tripID):
    try:
        itinerary = ItineraryEntry.objects.get(trip = tripID)
    except ItineraryEntry.DoesNotExist:
        return Response(status = status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = ItineraryEntrySerializer(itinerary)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = ItineraryEntrySerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)

@api_view(['GET', 'PUT', 'DELETE'])
def itinerary_details(request, userID, tripID, id):
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
