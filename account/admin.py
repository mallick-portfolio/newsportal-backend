from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# Register your models here.
from account.models import CustomUser

class UserAdmin(BaseUserAdmin):
  model = CustomUser

  list_display = ('email', 'username', 'first_name', 'last_name', 'is_active', 'is_superuser')
  list_filter = ('is_active', 'is_staff', 'is_superuser')
  fieldsets = (
      (None, {'fields': ('username', 'email', 'password', 'first_name', 'last_name', 'phone', 'gender', 'status',)}),
      ('Permissions', {'fields': ('is_staff', 'is_active','is_email_verified',
        'is_superuser', 'groups', 'user_permissions', )}),
      ('Dates', {'fields': ('last_login', 'date_joined')})
  )

  add_fieldsets = (
      (None, {
          'classes': ('wide',),
          'fields': ('username', 'email','first_name', 'last_name', 'phone', 'gender', 'status', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
  )
  search_fields = ('email',)
  ordering = ('email',)

admin.site.register(CustomUser, UserAdmin)