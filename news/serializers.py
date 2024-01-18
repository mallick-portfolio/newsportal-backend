from rest_framework import serializers
from news.models import Post, Category, PostAttachment
from account.serializers import UserSerializer
from account.models import CustomUser



class CategorySerializer(serializers.ModelSerializer):
  class Meta:
    model = Category
    fields = "__all__"


class PostAttachmentSerializer(serializers.ModelSerializer):
  class Meta:
    model = PostAttachment
    fields = "__all__"

class PostSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField('get_category')
    author = serializers.SerializerMethodField('get_author')

    class Meta:
        model = Post
        fields = "__all__"
        read_only_field = ['category', 'author']


    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.category = validated_data.get('category', instance.category)
        instance.save()
        return instance

    @staticmethod
    def get_category(obj):
      return CategorySerializer(obj.category).data

    @staticmethod
    def get_author(obj):
       return UserSerializer(obj.author).data

