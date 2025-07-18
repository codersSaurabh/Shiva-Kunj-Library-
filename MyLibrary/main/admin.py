
# Register your models here.
from django.contrib import admin
from .models import Booking  # Make sure Booking is imported
admin.site.register(Booking)