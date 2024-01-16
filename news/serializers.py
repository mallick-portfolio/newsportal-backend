from rest_framework import serializers
from news.models import News, Category
from account.serializers import UserSerializer
from account.models import CustomUser



class CategorySerializer(serializers.ModelSerializer):
  class Meta:
    model = Category
    fields = "__all__"

class NewsSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField('get_category')
    author = serializers.SerializerMethodField('get_author')

    class Meta:
        model = News
        fields = "__all__"
        read_only_field = ['category', 'author']

    @staticmethod
    def get_category(obj):
      return CategorySerializer(obj.category).data

    @staticmethod
    def get_author(obj):
       return UserSerializer(obj.author).data

