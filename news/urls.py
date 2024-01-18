from django.urls import path
from news import views


urlpatterns = [
    path("", views.NewsAPIView.as_view(), name="NewsAPIView"),
    path("<int:id>/", views.NewsAPIView.as_view(), name="NewsAPIViewDetails"),
    path("public/", views.PublicPostAPIView.as_view(), name="PublicPostAPIView"),
    path("public/<int:id>/", views.PublicPostAPIView.as_view(), name="PublicPostAPIView"),
    path("public/category/", views.PublicCategoryAPIView.as_view(), name="PublicCategoryAPIView"),
    path("attachment/", views.PostAttachmentAPIView.as_view(), name="PostAttachmentAPIView"),
    path("category/", views.CategoryAPIView.as_view(), name="CategoryAPI"),
    path("category/<int:id>/", views.CategoryAPIView.as_view(), name="CategoryDetailsAPI"),
]
