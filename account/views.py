from django.shortcuts import render, redirect
from .serializers import RegistrationSerializer, UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login, logout
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
import random
from rest_framework.decorators import (api_view, permission_classes, authentication_classes)
from rest_framework.permissions import IsAuthenticated
from account.models import CustomUser
import traceback
from account.helper import email_template
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from account import helper
from django.conf import settings

@api_view(['GET'])
def activate(request, uid64, token):
    try:
        uid = urlsafe_base64_decode(uid64).decode()
        user = CustomUser.objects.get(pk=uid)
        print(user)
    except(CustomUser.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_email_verified = True
        user.save()
        return Response({
          "success": True,
          "status": status.HTTP_201_CREATED,
          'message': "Email verify successfully!!!"
        })
    else:
        return Response({
          "success": True,
          "status": status.HTTP_201_CREATED,
          'message': "Failed to verify email!!!"
        })



class RegistrationAPIView(APIView):
  def post(self, request):
    try:
      data = request.data
      serializer = RegistrationSerializer(data=data)
      if serializer.is_valid():
        email = request.data['email']
        user = serializer.save()
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.id))
        confirm_link = f"{settings.BACKEND_DOMAIN}/api/v1/account/active/{uid}/{token}"
        email_data = {}
        email_data['confirm_link'] = confirm_link
        email_template(email, email_data, 'Verify email address', './email/verify_email.html')
        return Response({
          "success": True,
          "status": status.HTTP_201_CREATED,
          'message': "Registration successfull!!!. Please check your email."
        })
      else:
        return Response({
          "success": False,
          "status": status.HTTP_400_BAD_REQUEST,
          'message': "Registration failed.Username or email already exist",
          'error': True
        })
    except Exception as e:
      return Response({'message':'fail','error':e,"status": status.HTTP_500_INTERNAL_SERVER_ERROR})







class LoginAPIView(APIView):
  def post(self, request):
    try:
      rd = request.data
      if 'email' not in rd or 'password' not in rd:
        return Response({
          "success": False,
          'message': "Invalid Credentials",
        })
      email = rd['email']
      password = rd['password']
      user = authenticate(request, email=email, password=password)
      if user is not None and user.is_email_verified:
        login(request, user=user)
        token = helper.get_tokens_for_user(user)
        return Response({
          "success": True,
          'message': "Login successfull!!!",
          "token": token
        })
      else:
        return Response({
          "success": False,
          'message': "Invalid Credentials",
          "error": True
        })

    except Exception as e:
      return Response({'message':'fail','error':e,"status": status.HTTP_500_INTERNAL_SERVER_ERROR})


class LogoutAPIView(APIView):
  permission_classes = [IsAuthenticated]
  authentication_classes =[JWTAuthentication]
  def post(self, request):
    logout(request)
    return Response({
        "success": True,
        'message': "Successfully Logged out!!!",
        })

class MeAPI(APIView):
  authentication_classes = [JWTAuthentication]
  permission_classes = [IsAuthenticated]

  def get(self, request):
    try:
      user = CustomUser.objects.filter(email=request.user.email).first()
      data = UserSerializer(user, many=False).data
      print(data)

      if user is not None:
        return Response({
          "success": True,
          "status": status.HTTP_200_OK,
          'message': "Profile retrived successfully!!!",
          "data":data
          })
      else:
        return Response({
          "success": False,
          "status": status.HTTP_404_NOT_FOUND,
          'message': "Invalid user",
          })
    except Exception as e:
      return Response({
          "success": False,
          "status": status.HTTP_404_NOT_FOUND,
          'message': "Invalid user",
          "error": f"the following error are : {e}"
          })