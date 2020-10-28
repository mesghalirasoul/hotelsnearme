from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

class Property(models.Model):
    title = models.CharField(max_length=200)
    # vicinity = models.CharField(max_length=200)
    # highlightedVicinity = models.CharField(max_length=200)
    latitude = models.FloatField(default=0.0)
    longitude = models.FloatField(default=0.0)
    property_id = models.CharField(max_length=600)

    def __str__(self):
        return f"{self.title}"


class Booking(models.Model):
    customer_name = models.CharField(max_length=50)
    customer_phone_number = models.CharField(max_length=15)
    customer_email = models.EmailField(max_length=70,blank=True, null= True, unique= True)
    checkin_date = models.DateField()
    checkout_date = models.DateField()
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True)

 