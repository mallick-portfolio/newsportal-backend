from rest_framework import serializers
from news.models import News, Category
from account.serializers import UserSerializer



class CategorySerializer(serializers.ModelSerializer):
  class Meta:
    model = Category
    fields = "__all__"


class NewsSerializer(serializers.ModelSerializer):
  category = CategorySerializer()
  author = UserSerializer()
  class Meta:
    model = News
    fields = "__all__"

