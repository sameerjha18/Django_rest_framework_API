from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from django.core.mail import send_mail
from .models import OTP
from .serializers import EmailSerializer, OTPSerializer, RegisterSerializer
from django.utils import timezone
import random
from rest_framework_simplejwt.tokens import RefreshToken


class SendOTPView(APIView): # APIView which provides the basic view functionality for handling HTTP requests
    def post(self, request):
        serializer = EmailSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            # Checking that email that user provided is in the database or not if not then Otp won't be send and through 404 error.
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({"error": "User with this email does not exit."}, status=status.HTTP_400_BAD_REQUEST)
            

            otp_code = str(random.randint(100000, 999999))
            OTP.objects.create(user=user, otp_code=otp_code)
            send_mail(
                'Your OTP Code',
                f'Your OTP code is {otp_code}',
                'no-reply@example.com',
                [email],
                fail_silently=False
            )
            return Response({"message": "OTP sent to your email."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyOTPView(APIView):
    def post(self, request):
        serializer = OTPSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            otp_code = serializer.validated_data['otp_code']
            try:
                user = User.objects.get(email=email)
                otp = OTP.objects.get(user=user, otp_code=otp_code, valid_until__gte=timezone.now())
            except (User.DoesNotExist, OTP.DoesNotExist):
                return Response({"error": "Invalid OTP or OTP has expired"}, status=status.HTTP_400_BAD_REQUEST)
            
            otp.delete() # Delete OTP after successful verification

            # Create JWT token
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            
            return Response({
                "message": "Login successful.",
                "access_token": access_token,
                "refresh_token": str(refresh)
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Registration successful. Please verify your email."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)