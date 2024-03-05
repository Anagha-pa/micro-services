import random
from django.utils import timezone
from django.conf import settings
from django.core.cache import cache
from ..emails import send_otp_via_email
from ..utils import get_token_for_user
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import CustomUser
from .serializers import *




class RegisterView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        data = request.data
        serializer = RegisterSerializer(data=data)
        if serializer.is_valid():
            user = serializer.save()
            otp = ''.join([str(random.randint(0, 9)) for _ in range(settings.OTP["OTP_DIGIT_LENGTH"])])
            otp_expiration_time = timezone.now() + settings.OTP["OTP_EXPIRATION_TIME"]
            cache.set(user.email, otp, timeout=settings.OTP["OTP_EXPIRATION_TIME"].seconds)
            send_otp_via_email(user.email,otp)
            return Response(
                {
                    'status':200,
                    'message': f'An OTP is send to {user.email} Successfully',
                    'data':serializer.data
                }
            )
        return Response(
            {
                'status':400,
                'message':'User with this email is already exists',
                'error':serializer.errors
            }
        )



class VerifyOTPView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        data = request.data
        serializer = EmailOTPSerializer(data=data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            otp = request.data.get('otp')
            stored_otp = cache.get('email')
            if stored_otp == otp:
                user = CustomUser.objects.get(email=email)
                user.email_verified = True
                user.save()
                #delete otp from cache
                cache.delete(email)
                return Response({'message': 'Email verified successfully.'}, status=200)
            else:
                return Response({'message': 'Invalid OTP. Please try again.'}, status=400)
        return Response(serializer.errors, status=400)



class LoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        data = request.data
        serializer = LoginSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        token = get_token_for_user(user)
        return Response(
            {
                'status':200,
                'msg' : 'Login Success',
                'token' : token
            }
        )
    

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request):
        try:
           
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(
                {
                    'status':200,
                    'message':'Logout successful'
                }
            )
        except Exception as e:
            return Response(
                {
                    'status':500,
                    'error':str(e)
                }
            )









    