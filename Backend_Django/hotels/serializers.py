import logging
from rest_framework import serializers
from .models import Property, Booking
from django.core.validators import MinValueValidator, MaxValueValidator
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework.validators import UniqueValidator

###########
# Logging #
###########
logger = logging.getLogger(__name__)

class PropertySerializer(serializers.Serializer):
    # id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=200)
    vicinity = serializers.CharField(max_length=200)
    highlightedVicinity = serializers.CharField(max_length=200)
    latitude = serializers.FloatField(default=0.0)
    longitude = serializers.FloatField(default=0.0)
    property_id = serializers.CharField(max_length=200)

    def create(self, validated_data):
        """
        Create and return a new `Property` instance, given the validated data.
        """

        return Property.objects.create(**validated_data)


class BookingSerializer(serializers.Serializer):
    class Property(serializers.Serializer):
        title = serializers.CharField(max_length=200)
        latitude = serializers.FloatField(default=0.0)
        longitude = serializers.FloatField(default=0.0)
        property_id = serializers.CharField(max_length=200)
    
    property = Property(source="*")
    customer_name = serializers.CharField(max_length=50)
    customer_phone_number = serializers.CharField(max_length=15)
    customer_email = serializers.EmailField(max_length=70,
                                            validators=[UniqueValidator(
                                            queryset=Booking.objects.all())])
    checkin_date = serializers.DateField()
    checkout_date = serializers.DateField()

    def create(self, validated_data):
        property, created = Property.objects.get_or_create(
       
            title = validated_data["title"],
            latitude = validated_data["latitude"],
            longitude = validated_data["longitude"],
            property_id = validated_data["property_id"]
        )
        
        booking, created = Booking.objects.get_or_create(
  
            customer_name = validated_data["customer_name"],
            customer_phone_number = validated_data["customer_phone_number"],
            customer_email = validated_data["customer_email"],
            checkin_date = validated_data["checkin_date"],
            checkout_date = validated_data["checkout_date"],
            property = property
        )

        return booking

    def validate(self, data):
        if data["checkin_date"] > data["checkout_date"]:
            raise serializers.ValidationError("checkout date must be after checkin date.")

        if len(data["customer_phone_number"]) > 15:
            raise serializers.ValidationError("customer_phone_number must be a valid number")

        return data

class BookingForAPropertySerializer(serializers.ModelSerializer):
    property = serializers.StringRelatedField()

    class Meta:
        model = Booking
        fields = ["property",
                "customer_name",
                "customer_phone_number",
                "customer_email",
                "checkin_date",
                "checkout_date"]
     
