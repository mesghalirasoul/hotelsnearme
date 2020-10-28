from django.test import TestCase

import json
import time
import dotenv  # Support .env file
import os

from django.test import SimpleTestCase, TransactionTestCase
from django.contrib.auth.models import User
from django.urls import reverse, resolve

from rest_framework import status
from rest_framework.test import APITestCase
import rest_framework
from rest_framework import serializers

from hotels.models import Booking, Property
from .sample_payloads import payload1, payload2, payload3
from hotels.serializers import BookingSerializer


class BookingsView(APITestCase):
    allow_database_queries = True
    BASE_DIR = os.path.abspath(os.path.join(__file__ ,"../../.."))
    dotenv.read_dotenv(os.path.join(BASE_DIR,'.env')) # Support .env file
    APIKEY = os.environ.get("APIKEY", "localhost")
        
    def test_api(self):

        url = reverse('hotels:BookingsView')
        self.assertEqual(url, '/api/bookings')
        
        resolver = resolve('/api/bookings')
        self.assertEqual(resolver.view_name, 'hotels:BookingsView')

        data = json.loads(payload1)
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Booking.objects.count(),1)
        self.assertEqual(Property.objects.count(),1)
        
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Booking.objects.count(),1)
        self.assertEqual(Property.objects.count(),1)
      
        time.sleep(1) # we must wait to make sure data are inserted into DB
    
        data = json.loads(payload2)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Booking.objects.count(),2)
        self.assertEqual(Property.objects.count(),1)

        data = json.loads(payload3)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Booking.objects.count(),3)
        self.assertEqual(Property.objects.count(),2)

        Wrongdata = {**data}
        Wrongdata["customer_phone_number"] = "123456789123456324"
        response = self.client.post(url, Wrongdata, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        Wrongdata = {**data}
        Wrongdata["checkin_date"] = "2020-10-27"
        Wrongdata["checkout_date"] = "2020-10-22"
        response = self.client.post(url, Wrongdata, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_serializer(self):
    
        data = json.loads(payload1)

        #Check if the request payload is valid from serilializer perspective
        serialized_data = BookingSerializer(data=data)
        self.assertEqual(serialized_data.is_valid(), True)

        WrongPayload1 = {**data}
        WrongPayload1["checkin_date"] = "2020-10-27"
        WrongPayload1["checkout_date"] = "2020-10-22"

        CheckInData_validator = BookingSerializer(data=WrongPayload1)
        self.assertRaises(serializers.ValidationError, CheckInData_validator.is_valid, {"raise_exception": True})


        WrongPayload2 = {**data}
        WrongPayload2["customer_phone_number"] = "123456789123456324"
        PhoneNumber_validator = BookingSerializer(data=WrongPayload2)
        self.assertRaises(serializers.ValidationError, PhoneNumber_validator.is_valid, raise_exception= True)
