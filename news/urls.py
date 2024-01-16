from django.urls import path
from news import views


urlpatterns = [
    path("", views.NewsAPIView.as_view(), name="NewsAPIView"),
    path("category/", views.CategoryAPIView.as_view(), name="CategoryAPI"),
    path("category/<int:id>/", views.CategoryAPIView.as_view(), name="CategoryDetailsAPI"),
]
