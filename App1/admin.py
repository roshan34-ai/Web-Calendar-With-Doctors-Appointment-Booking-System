from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
#from App1.views import Specialist_list
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import User, CustomUser, Appointment_User



class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['specialist_name', 'email', 'phone', 'image', 'password', 'profession', 'locality', 'state_name', 'dist_name', 'experience', 'about', 'cunsultation_fees', 'is_staff', 'is_active']
    list_filter = ['email', 'is_staff', 'is_active',]
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)


# Register your models here
class UserAdmin(admin.ModelAdmin):
    list_display  = ['name', 'phone', 'email', 'date', 'from_time', 'specialist_name']

class Appointment_UserAdmin(admin.ModelAdmin):
    list_display  = ['name', 'phone', 'email', 'password']


#admin.site.register(cunsultant, cunsultantAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Appointment_User, Appointment_UserAdmin)


