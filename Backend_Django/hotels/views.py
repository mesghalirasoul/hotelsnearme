
# Core
import os
import logging
import datetime
from threading import Timer
import requests

# Third-party
from django.core.cache import cache
from django.shortcuts import render
from django.db.utils import NotSupportedError
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework.exceptions import APIException
from rest_framework.exceptions import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import exception_handler
from rest_framework.renderers import JSONRenderer

# Project
from hotels.helpers.renderers import CustomJSONRenderer
from hotels.helpers.mesure_duration import MeasureDuration
from .models import Booking, Property
from .serializers import PropertySerializer, BookingSerializer, BookingForAPropertySerializer
from .utils import HereApiService

###########
# Logging #
###########
logger = logging.getLogger(__name__)


class PropertiesView(APIView):
    """
    API endpoint that receives data and reply with corresponding
        score data

    TODO: Should only work for POST types
    """

    # queryset = Hotels.objects.all()
    # serializer_class = serializers.Hotelserializers
    # renderer_classes = [CustomJSONRenderer]
    # permission_classes = [HasAPIKey]


    def get(self, request):

        location = request.GET['at']
        Lat,Long = location.split(',')
        Lat = float(Lat)
        Long = float(Long)
     
        CACHED_Location = '_'.join(["location",
                                    str(Lat),
                                    str(Long)])

        # Redis cache to increase performance of this API and decrease number of HEREAPI call.
        if CACHED_Location in cache:
            result = cache.get(CACHED_Location)
        else:
            result = HereApiService("hotel", Lat, Long)
            cache.set(CACHED_Location, result, timeout = 864000)
            logger.info("data are cached in redis")
        
        return Response(result,status=status.HTTP_200_OK)

    def http_method_not_allowed(self, request, *args, **kwargs):
        raise MethodNotAllowed(method = request.method, detail=f'{request.method} is an invalid method type', 
                                code='Method Not Allowed')


class BookingsView(APIView):
    """
    API endpoint that receives data and inserts into database
    """

    # XXX .order_by('-created') # check syntax here .. probably needs a verbose name
    # queryset = Property.objects.all()
    serializer_class = BookingSerializer
    # renderer_classes = [CustomJSONRenderer]
    # permission_classes = [HasAPIKey]


    def post(self, request):
        with MeasureDuration('Serialization => Serializing Data') as m:
            serializer = BookingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        logger.debug("Valid record received")
        saved: HotelRecord = serializer.save()

        content = {'data':request.data}
        message = 'Data Successfully inserted'
        logger.info("Data Successfully inserted")
        return Response([content,message],status=status.HTTP_201_CREATED)
    
    def http_method_not_allowed(self, request, *args, **kwargs):
        raise MethodNotAllowed(method = request.method, detail=f'{request.method} is an invalid method type', 
                                code='Method Not Allowed')
        

class BookingsForAPropertyView(APIView):

    renderer_classes = [CustomJSONRenderer]

    def get(self, request, PROPERTY_ID):
    
        try:
            with MeasureDuration('SQL Query => Load data') as m:
                bookings = Booking.objects.filter(property__property_id=PROPERTY_ID)
            with MeasureDuration('Serialization => Serializing Data') as m:
                serializer = BookingForAPropertySerializer(bookings, many = True)
                content = serializer.data

            message = "Data successfully retrieved"
            logger.info("Data successfully retrieved")
            return Response([content,message],status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            raise NotFound(detail="The required data does not exist!", code="404 Not Found")
    
    def http_method_not_allowed(self, request, *args, **kwargs):
        raise MethodNotAllowed(method = request.method, detail=f'{request.method} is an invalid method type', 
                                code='Method Not Allowed')