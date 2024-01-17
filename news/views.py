from django.shortcuts import render, redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
import random
from rest_framework.decorators import (api_view, permission_classes, authentication_classes)
from rest_framework.permissions import IsAuthenticated
from account.models import CustomUser
from news.models import News, Category
from news.serializers import NewsSerializer, CategorySerializer
import traceback
from account.helper import email_template
from account import helper
from news import helpers
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404



class NewsAPIView(APIView):
  permission_classes=[IsAuthenticated]
  authentication_classes = [JWTAuthentication]

  def get(self, request):
    try:
      categories = Category.objects.all()
      data = CategorySerializer(categories, many=True).data
      return Response({
          "success": True,
          "message": "Categories retrived successfully!!!",
          "error": False,
          "data": data
        }, status=status.HTTP_200_OK)
    except Exception as e:
      return Response({
          "error": f'Error is {e}',
          'trackback': "".join(traceback.format_exception(type(e), e, e.__traceback__))
        })

  @method_decorator(helpers.admin_only)
  def post(self, request):
    try:
      data = request.data
      category_id = data.get('category')
      category = Category.objects.get(id=category_id)
      serializer = NewsSerializer(data=request.data)


      if serializer.is_valid():
        serializer.save(author=request.user, category=category)
        return Response({
          "success": True,
          "message": "Post created!!!",
          "error": False,
          "data": serializer.data
        }, status=status.HTTP_200_OK)
      else:
        print(serializer.errors)
        return Response({
          "success": False,
          "message": "Post already exit with this name. ",
          "error": True,
          "ta": serializer.errors
        }, status=status.HTTP_200_OK)
    except Exception as e:
      return Response({
          "error": f'Error is {e}',
          'trackback': "".join(traceback.format_exception(type(e), e, e.__traceback__))
        })


  @method_decorator(helpers.admin_only)
  def delete(self, request, id):
    try:
      category = Category.objects.filter(id=id).first()
      if category is not None:
        category.delete()
        return Response({
            "success": True,
            "message": "Category deleted successfully!!!",
            "error": False,
          }, status=status.HTTP_200_OK)
      else:
        return Response({
            "success": False,
            "message": "Failed to delete category!!!",
            "error": False,
          }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
      return Response({
          "error": f'Error is {e}',
          'trackback': "".join(traceback.format_exception(type(e), e, e.__traceback__))
        })
class CategoryAPIView(APIView):
  permission_classes=[IsAuthenticated]
  authentication_classes = [JWTAuthentication]

  def get(self, request):
    try:
      categories = Category.objects.all()
      data = CategorySerializer(categories, many=True).data
      return Response({
          "success": True,
          "message": "Categories retrived successfully!!!",
          "error": False,
          "data": data
        }, status=status.HTTP_200_OK)
    except Exception as e:
      return Response({
          "error": f'Error is {e}',
          'trackback': "".join(traceback.format_exception(type(e), e, e.__traceback__))
        })

  @method_decorator(helpers.admin_only)
  def post(self, request):
    try:
      serializer = CategorySerializer(data=request.data)
      if serializer.is_valid():
        serializer.save()
        return Response({
          "success": True,
          "message": "Category created!!!",
          "error": False,
          "data": serializer.data
        }, status=status.HTTP_200_OK)
      else:
        return Response({
          "success": False,
          "message": "Category already exit with this name. ",
          "error": True,
        }, status=status.HTTP_200_OK)
    except Exception as e:
      return Response({
          "error": f'Error is {e}',
          'trackback': "".join(traceback.format_exception(type(e), e, e.__traceback__))
        })


  @method_decorator(helpers.admin_only)
  def delete(self, request, id):
    try:
      category = Category.objects.filter(id=id).first()
      if category is not None:
        category.delete()
        return Response({
            "success": True,
            "message": "Category deleted successfully!!!",
            "error": False,
          }, status=status.HTTP_200_OK)
      else:
        return Response({
            "success": False,
            "message": "Failed to delete category!!!",
            "error": False,
          }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
      return Response({
          "error": f'Error is {e}',
          'trackback': "".join(traceback.format_exception(type(e), e, e.__traceback__))
        })