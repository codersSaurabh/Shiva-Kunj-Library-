# models.py
from django.db import models
from django.utils import timezone

class Booking(models.Model):
    name = models.CharField(max_length=100,default="")
    mobile = models.CharField(max_length=15,default="NA")
    aadhar = models.CharField(max_length=12,default="NA")
    shift = models.CharField(max_length=20,default="")
    sheet_number = models.PositiveIntegerField(default=0) # 1 to 105
    booking_date = models.DateTimeField(default=timezone.now)
    fee_status = models.CharField(max_length=10, choices=[('Paid', 'Paid'), ('Unpaid', 'Unpaid')], default='Unpaid')
    email = models.CharField(max_length=25,default="NA")
    def __str__(self):
        return f"{self.name} ({self.mobile})"
