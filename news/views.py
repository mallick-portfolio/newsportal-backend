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
from news.models import Post, Category, PostRating
from news.serializers import (PostSerializer,
                              CategorySerializer,
                              PostAttachmentSerializer,
                              PostRatingSerializer)
import traceback
from account.helper import email_template
from account import helper
from news import helpers
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404
from account.helper import email_template
from django.views.decorators.csrf import csrf_exempt



class PostAttachmentAPIView(APIView):
  @csrf_exempt
  def post(self, request):
    try:
      data = request.data
      serializer = PostAttachmentSerializer(data=request.data)
      if serializer.is_valid():
        serializer.save()
        return Response({
            "success": True,
            "message": "Attachment uploaded!!!",
            "error": False,
            "data": serializer.data
          }, status=status.HTTP_200_OK)
      else:
        return Response({
            "success": False,
            "message": "Attachment failed!!!",
            "error": True,
            "data": serializer.errors
          }, status=status.HTTP_200_OK)

    except Exception as e:
      return Response({
          "error": f'Error is {e}',
          'trackback': "".join(traceback.format_exception(type(e), e, e.__traceback__))
        })


class NewsAPIView(APIView):
  permission_classes=[IsAuthenticated]
  authentication_classes = [JWTAuthentication]

  @method_decorator(helpers.admin_only)
  def get(self, request, id=None):
    try:
      if id is not None:
        post = Post.objects.filter(id=id).first()
        data = PostSerializer(post).data
        return Response({
            "success": True,
            "message": "Post retrived successfully!!!",
            "error": False,
            "data": data
          }, status=status.HTTP_200_OK)
      else:
        posts = Post.objects.all()
        data = PostSerializer(posts, many=True).data
        return Response({
            "success": True,
            "message": "Posts retrived successfully!!!",
            "error": False,
            "data": data
          }, status=status.HTTP_200_OK)
    except Exception as e:
      return Response({
          "error": f'Error is {e}',
          'trackback': "".join(traceback.format_exception(type(e), e, e.__traceback__))
        })

  @method_decorator(helpers.admin_only)
  @csrf_exempt
  def post(self, request):
    try:
      data = request.data
      category_id = data.get('category')
      category = Category.objects.get(id=category_id)
      serializer = PostSerializer(data=request.data)

      if serializer.is_valid():
        serializer.save(author=request.user, category=category)
        return Response({
          "success": True,
          "message": "Post created!!!",
          "error": False,
          "data": serializer.data
        }, status=status.HTTP_200_OK)
      else:
        return Response({
          "success": False,
          "message": "Something want wrong",
          "error": True,
        }, status=status.HTTP_200_OK)
    except Exception as e:
      return Response({
          "error": f'Error is {e}',
          'trackback': "".join(traceback.format_exception(type(e), e, e.__traceback__))
        })


  @method_decorator(helpers.admin_only)
  @csrf_exempt
  def put(self, request, id):
    try:
      post = Post.objects.filter(id=id).first()
      if post is not None:
        serializer = PostSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
          serializer.save()
          return Response({
            "success": True,
            "message": "Post updated successfully!!!",
            "error": False,
            "data": serializer.data
          }, status=status.HTTP_200_OK)
        else:
          return Response({
            "success": False,
            "message": "Failed to update post!!!",
            "error": True,
          }, status=status.HTTP_200_OK)
      else:
        return Response({
            "success": False,
            "message": "Invalid post id!!!",
            "error": True,
          }, status=status.HTTP_200_OK)
    except Exception as e:
      return Response({
          "error": f'Error is {e}',
          'trackback': "".join(traceback.format_exception(type(e), e, e.__traceback__))
        })


  @method_decorator(helpers.admin_only)
  @csrf_exempt
  def delete(self, request, id):
    try:
      post = Post.objects.filter(id=id).first()
      if post is not None:
        post.delete()
        return Response({
            "success": True,
            "message": "Post deleted successfully!!!",
            "error": False,
          }, status=status.HTTP_200_OK)
      else:
        return Response({
            "success": False,
            "message": "Failed to delete post!!!",
            "error": False,
          }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
      return Response({
          "error": f'Error is {e}',
          'trackback': "".join(traceback.format_exception(type(e), e, e.__traceback__))
        })


class PublicPostAPIView(APIView):

  def get(self, request, id=None):
    try:
      if id is not None:
        post = Post.objects.filter(id=id).first()
        data = PostSerializer(post).data
        return Response({
            "success": True,
            "message": "Post retrived successfully!!!",
            "error": False,
            "data": data
          }, status=status.HTTP_200_OK)
      else:
        category = request.query_params.get('category')
        print("category", category)
        if category is not None:
          posts = Post.objects.filter(category__slug=category)
          print("posts", posts)
        else:
          posts = Post.objects.all()
        data = PostSerializer(posts, many=True).data
        return Response({
            "success": True,
            "message": "Posts retrived successfully!!!",
            "error": False,
            "data": data
          }, status=status.HTTP_200_OK)
    except Exception as e:
      return Response({
          "error": f'Error is {e}',
          'trackback': "".join(traceback.format_exception(type(e), e, e.__traceback__))
        })


class PublicCategoryAPIView(APIView):

  def get(self, request, id=None):
    try:
      if id is not None:
        category = Category.objects.filter(id=id).first()
        data = CategorySerializer(category).data
        return Response({
            "success": True,
            "message": "Post retrived successfully!!!",
            "error": False,
            "data": data
          }, status=status.HTTP_200_OK)
      else:
        category = Category.objects.all()
        data = CategorySerializer(category, many=True).data
        return Response({
            "success": True,
            "message": "Posts retrived successfully!!!",
            "error": False,
            "data": data
          }, status=status.HTTP_200_OK)
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
  @csrf_exempt
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
  @csrf_exempt
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


class PostRatingAPIView(APIView):
  permission_classes=[IsAuthenticated]
  authentication_classes = [JWTAuthentication]

  @csrf_exempt
  def post(self, request, id):

    try:

      data = request.data
      data['user'] = request.user.id
      post = Post.objects.filter(id=id).first()
      data['post'] = post.id
      print(data)

      if post is not None:
        serializer = PostRatingSerializer(data=data)
        if serializer.is_valid():
          serializer.save()
          email_template(request.user.email, "email_data", 'Post rating', './email/post_rating.html')
          return Response({
            "success": True,
            "message": "Rating added successfully",
            "error": False,
            "data": serializer.data
          }, status=status.HTTP_200_OK)
        else:
          return Response({
            "success": False,
            "message": "Failed to add rating ",
            "error": True,
            "dte": serializer.errors
          }, status=status.HTTP_200_OK)
      else:
        return Response({
            "success": False,
            "message": "Invalid post id",
            "error": True,
          }, status=status.HTTP_200_OK)
    except Exception as e:
      return Response({
          "error": f'Error is {e}',
          'trackback': "".join(traceback.format_exception(type(e), e, e.__traceback__))
        })

