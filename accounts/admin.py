from django.contrib import admin
from .models import User
from .models import UserProfile
from django.contrib.auth.admin import UserAdmin

# Register your models here.
admin.site.register(UserProfile)

class CustomUserAdmin(UserAdmin): 
    list_display = ('email', 'first_name', 'last_name', 'username', 'role', 'is_active')# without this the admin dashboard
    #would display only default values but with this we can specify what to display. These fields are coming from class User(AbstractBaseUser):
    ordering = ('-date_joined',)# to make the password no editable line 9, 12, 13, 14, 15 and 18 would do
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(User, CustomUserAdmin)


