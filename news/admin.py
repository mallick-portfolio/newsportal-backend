from django.contrib import admin
from .models import Post, Category, PostAttachment
# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
  readonly_fields = ['slug',]


class PostAdmin(admin.ModelAdmin):
  readonly_fields = ['slug',]


admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(PostAttachment)