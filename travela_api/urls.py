"""
URL configuration for travela_api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from django.conf import settings
from django.conf.urls.static import static

from travela_api import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', views.users_list),
    path('users/<str:userID>/', views.user_details),
    path('users/<str:userID>/trips/', views.user_trips),
    path('users/<str:userID>/trips/<int:id>/', views.trip_details),
    path('users/<str:userID>/trips/<int:tripID>/itineraryEntry/', views.itinerary_list),
    path('users/<str:userID>/trips/<int:tripID>/itineraryEntry/<int:id>/', views.itinerary_details),
]
if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)