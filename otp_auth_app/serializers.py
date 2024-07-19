# DRF Serializer is used to convert the complex data type such as queryset and model instance, 
# into native python datatypes that can then be easily rendered into json, xml, and other contect types.
from rest_framework import serializers
from django.contrib.auth.models import User


class EmailSerializer(serializers.Serializer): # This serializer will ensure that the input data for the email field is a valid email address.
    email = serializers.EmailField()


class OTPSerializer(serializers.Serializer): # This serializer will ensure that the input data for OTPSerializer the email is valid and the otp code is string and upto 6 digit.
    email = serializers.EmailField()
    otp_code = serializers.CharField(max_length=6)

# This register Serializer is inherit from serializers.modelserializer.
# Using modelserializer provides a shortcut that includes default implementation for creating, updating, and validating objects based on model
class RegisterSerializer(serializers.ModelSerializer):
    class Meta: # A nested class that provides metadata about serializer.
        model = User # This serializer is associated with User model.
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}} # It makes the password field write only meaning it will be used for creating and updating objects but won't be included


    # This funcionality is ensuring that the user email is unique and if the user send duplicate it will raise error.
    def Validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(" A user with this email already exists.")
        return value
    

    # The create method handles the creation of a new user. It sets the username, email, and hashed password, then save the user to the database.
    def create(self, validated_data):
        user = User(
            username = validated_data['username'],
            email = validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user