
from django.conf.urls import url
from django.urls import path
from rest_framework import permissions, routers, urls
from hotels.views import PropertiesView, BookingsView, BookingsForAPropertyView


# Add the internal routes
# See https://www.django-rest-framework.org/api-guide/routers/#usage for how the names for the views are generated
router = routers.DefaultRouter()

urlpatterns = [
    url(r'^properties/$',PropertiesView.as_view(), name='PropertiesView'),
    url(r'^bookings$',BookingsView.as_view(), name='BookingsView'),
    url(r'^properties/(?P<PROPERTY_ID>.*)/bookings$',BookingsForAPropertyView.as_view(), name='BookingsForAPropertyView'), 
]

urlpatterns = urlpatterns + router.urls

app_name = 'hotels'
