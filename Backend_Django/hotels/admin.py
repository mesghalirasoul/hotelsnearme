from django.contrib import admin

# Register your models here.

# from django.contrib.gis.admin import OSMGeoAdmin
from .models import Property

admin.site.register(Property)