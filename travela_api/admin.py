from django.contrib import admin
from .models import *

admin.site.register(User)
admin.site.register(Trip)
admin.site.register(ItineraryEntry)
admin.site.register(HomeDestination)