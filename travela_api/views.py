from django.http import JsonResponse
from rest_framework.decorators import api_view
from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework import status
from .scraper import *
from datetime import date, timedelta
import random


#Funtion for list of users. Has get and post methods
@api_view(['GET', 'POST'])
def users_list(request):
    #Gets data of all users
    if request.method == 'GET':
        users = User.objects.all()
        serializer = UserSerializer(users, many = True)
        return Response(serializer.data)
    
    #Posts data of user
    elif request.method == 'POST':
        serializer = UserSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)


#Funtion for user detail. Has get, put and delete methods
@api_view(['GET', 'PUT', 'DELETE'])
def user_details(request, userID):
    #If the user does not exist returns error status
    try:
        user = User.objects.get(pk = userID)
    except User.DoesNotExist:
        return Response(status = status.HTTP_404_NOT_FOUND)

    #Gets the user data
    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(serializer.data)
    
    #Puts the user data(In case user edits the data)
    elif request.method == 'PUT':
        serializer = UserSerializer(user, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    #Deletes user
    elif request.method == 'DELETE':
        user.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)


#Funtion for user trips. Has get and post methods
@api_view(['GET', 'POST'])
def user_trips(request, userID):
    #If the trip does not exist returns error status
    try:
        trips = Trip.objects.filter(owner = userID)
    except Trip.DoesNotExist:
        return Response(status = status.HTTP_404_NOT_FOUND)
    
    #Gets all user trips
    if request.method == 'GET':
        serializer = TripSerializer(trips, many = True)
        return Response(serializer.data)
    
    #Posts or creates a user trip
    if request.method == 'POST':
        serializer = TripSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)


#Funtion for getting user pending trips. Has only get method
@api_view(['GET'])
def user_pending_trips(request, userID):
    #If the trip does not exist returns error status
    try:
        trips = Trip.objects.filter(pendingUsers__userEmail__contains = userID)
    except Trip.DoesNotExist:
        return Response(status = status.HTTP_404_NOT_FOUND)
    
    #Gets all pending trips of the user
    if request.method == 'GET':
        serializer = TripSerializer(trips, many = True)
        return Response(serializer.data)


#Funtion for getting user personal trips. Has only get method
@api_view(['GET'])
def user_personal_trips(request, userID):
    #If the trip does not exist returns error status
    try:
        trips = Trip.objects.filter(owner = userID).filter(sharedUsers__isnull=True)
    except Trip.DoesNotExist:
        return Response(status = status.HTTP_404_NOT_FOUND)
    
    #Gets all personal trips of the user
    if request.method == 'GET':
        serializer = TripSerializer(trips, many = True)
        return Response(serializer.data)


#Funtion for getting user group trips. Has only get method
@api_view(['GET'])
def user_group_trips(request, userID):
    #If the trip does not exist returns error status
    try:
        tripsA = Trip.objects.filter(owner = userID).filter(sharedUsers__isnull=False)
        tripsB = Trip.objects.filter(sharedUsers__userEmail__exact = userID)
        trips = tripsA.union(tripsB)
    except Trip.DoesNotExist:
        return Response(status = status.HTTP_404_NOT_FOUND)
    
    #Gets all group trips of the user
    if request.method == 'GET':
        serializer = TripSerializer(trips, many = True)
        return Response(serializer.data)
        

#Funtion for getting user trip details. Has get, put and delete methods
@api_view(['GET', 'PUT', 'DELETE'])
def trip_details(request, id):
    #If the trip does not exist returns error status
    try:
        trip = Trip.objects.get(pk = id)
    except Trip.DoesNotExist:
        return Response(status = status.HTTP_404_NOT_FOUND)

    #Gets the user trip details
    if request.method == 'GET':
        serializer = TripSerializer(trip)
        return Response(serializer.data)
    
    #Puts the user trip details (In case the user edits the details)
    elif request.method == 'PUT':
        serializer = TripSerializer(trip, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    
    #Deletes the user trip
    elif request.method == 'DELETE':
        trip.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)
    

#Funtion for getting itinerary list. Has get and post methods  
@api_view(['GET', 'POST'])
def itinerary_list(request, tripID): 
    #Gets the itinerary list 
    if request.method == 'GET':
        #If the itinerary does not exist returns error status
        try:
            entries = ItineraryEntry.objects.filter(trip = tripID).order_by('dateTime')
        except ItineraryEntry.DoesNotExist:
            return Response(status = status.HTTP_404_NOT_FOUND)
        serializer = ItineraryEntrySerializer(entries, many=True)
        return Response(serializer.data)
    
    #Posts the itinerary list
    elif request.method == 'POST':
        serializer = ItineraryEntrySerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)


#Funtion for getting itinerary details. Has get, put and delete methods  
@api_view(['GET', 'PUT', 'DELETE'])
def itinerary_details(request, tripID, id):
    #If the itinerary does not exist returns error status
    try:
        itinerary = ItineraryEntry.objects.get(pk = id)
    except ItineraryEntry.DoesNotExist:
        return Response(status = status.HTTP_404_NOT_FOUND)

    #Gets the itinerary details
    if request.method == 'GET':
        serializer = ItineraryEntrySerializer(itinerary)
        return Response(serializer.data)
    
    #Puts the itinerary details(In case user edits the itinerary entry)
    elif request.method == 'PUT':
        serializer = ItineraryEntrySerializer(itinerary, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    #Deletes the itinerary entry
    elif request.method == 'DELETE':
        itinerary.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)


#Funtion for destination search. Has only get method
@api_view(['GET'])
def destination_search(request, search_term):
    #Gets the destinations based off the search term
    if request.method == 'GET':
        return Response(getDestinations(search_term))


#Funtion for destination detail. Has only get method
@api_view(['GET'])
def destination_details(request, search_term):
    #Gets the destination detail based off the search term
    if request.method == 'GET':
        return Response(getDestinationDetails(search_term))


#Funtion for nearby destinations for a destination. Has only get method
@api_view(['GET'])
def destination_nearby(request):
    #Gets the nearby destinations based off the longitude and latitude
    if request.method == 'GET':
        latitude = request.GET.get('latitude')
        longitude = request.GET.get('longitude')
        return Response(getNearbyPlaces(latitude, longitude))


#Funtion for destination location. Has only get method
@api_view(['GET'])
def destination_location(request, search_term):
    #Gets the destination location based off the search term
    if request.method == 'GET':
        return Response(getDestinationLocation(search_term))


#Funtion for nearby destinations for a user location. Has only get method
@api_view(['GET'])
def nearby_destinations(request):
    #Gets the nearby destinations based off the longitude and latitude
    if request.method == 'GET':
        latitude = request.GET.get('latitude')
        longitude = request.GET.get('longitude')
        return Response(getNearbyDestinations(latitude, longitude))


#Funtion for home screen banner. Has only get method    
@api_view(['GET'])
def home_banner(request):
    #If a destination for home banner could not be found returns error message
    try:
        destinationSet = HomeDestination.objects.all()
        destination = random.choice(destinationSet)
    except HomeDestination.DoesNotExist:
        return Response(status = status.HTTP_404_NOT_FOUND)
    
    #Gets the home banner destination
    if request.method == 'GET':
        serializer = DestinationSerializer(destination) 
        return Response(serializer.data)


#Funtion for home hot destinations. Has only get method     
@api_view(['GET'])
def home_hot_destination(request):
    #If home hot destinations could not be found returns error message
    try:
        destinationSet = list(HomeDestination.objects.all())
        destinations = random.sample(destinationSet, 10)
    except HomeDestination.DoesNotExist:
        return Response(status = status.HTTP_404_NOT_FOUND)

    #Gets the home hot destinations
    if request.method == 'GET':
        serializer = DestinationSerializer(destinations, many=True)
        return Response(serializer.data)


#Funtion for home filter. Has only get method 
@api_view(['GET'])
def home_filter(request, tag_name):
    #If home filtered data could not be found returns error message
    try:
        destinations = HomeDestination.objects.filter(destinationTag=tag_name)
    except HomeDestination.DoesNotExist:
        return Response(status = status.HTTP_404_NOT_FOUND)

    #Gets the home filtered data
    if request.method == 'GET':
        serializer = DestinationSerializer(destinations, many=True)
        return Response(serializer.data)


#Funtion for home location of the day. Has only get method 
@api_view(['GET'])
def home_location_of_the_day(request):
    #If home location of the day could not be found returns error message
    try:
        locations = HomeDestination.objects.values_list('destinationLocation', flat=True).distinct()
        seed = int(date.today().strftime('%Y%m%d'))
        generator = random.Random(seed)
        new_location = generator.choice(locations)
        location_data = HomeDestination.objects.filter(destinationLocation=new_location)
    except HomeDestination.DoesNotExist:
        return Response(status = status.HTTP_404_NOT_FOUND)

    #Gets the home location of the day
    if request.method == 'GET':
        serializer = DestinationSerializer(location_data, many=True)
        return Response(serializer.data)


#Funtion for filtered home location of the day. Has only get method 
@api_view(['GET'])
def home_location_of_the_day_filtered(request, tag_name):
    #If filtered home location of the day could not be found returns error message
    try:
        locations = HomeDestination.objects.values_list('destinationLocation', flat=True).distinct()
        seed = int(date.today().strftime('%Y%m%d'))
        generator = random.Random(seed)
        new_location = generator.choice(locations)
        location_data = HomeDestination.objects.filter(destinationLocation=new_location).filter(destinationTag=tag_name)
    except HomeDestination.DoesNotExist:
        return Response(status = status.HTTP_404_NOT_FOUND)

    #Gets the filtered home location of the day
    if request.method == 'GET':
        serializer = DestinationSerializer(location_data, many=True)
        return Response(serializer.data)