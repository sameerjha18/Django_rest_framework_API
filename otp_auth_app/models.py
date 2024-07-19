from django.db import models
from django.contrib.auth.models import User # Used Built-in User Model for handling user account
from django.utils import timezone # Utility functions for handling time zones.
import datetime

# Created an OTP model which define table in database
class OTP(models.Model):
    # Defining relation between OTP and User table and setting up like if the user is deleted the otp related to the use will also deleted.
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    otp_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    valid_until = models.DateTimeField()
    
    # This method is Overridden to add custome behaviour before saving an OTP Instance
    def save(self, *args, **kwargs):
        if not self.valid_until: # Checking if the valid_until is not set
            self.valid_until = timezone.now() + datetime.timedelta(minutes=5) # Seting the valid_until to time now and add 5 min to it for validation of OTP
        super().save(*args, **kwargs) # Calling the parent class's save method to ensure the object is saved to the database.