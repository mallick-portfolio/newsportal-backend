from django.contrib import admin
from .models import News, Category
# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
  readonly_fields = ['slug',]


class NewsAdmin(admin.ModelAdmin):
  readonly_fields = ['slug',]


admin.site.register(News, NewsAdmin)
admin.site.register(Category, CategoryAdmin)