from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager
from django.template.defaultfilters import date


class CustomUser(AbstractBaseUser, PermissionsMixin):
    specialist_name = models.CharField(max_length=100, blank=False, null=False)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=13)
    image = models.ImageField(upload_to='profile/', default='default.jpg', blank=True, null=False)
    password = models.CharField(max_length=100)
    profession = models.CharField(max_length=100)
    qualification=models.CharField(max_length=100)
    locality = models.CharField(max_length=100, null=True, blank=True)
    state_name = models.CharField(max_length=100)
    dist_name = models.CharField(max_length=100)
    pincode=models.CharField(max_length=10)
    experience=models.CharField(max_length=10)
    about = models.CharField(max_length=200)
    cunsultation_fees = models.CharField(max_length=5)
    
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ""   
        return url
    

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.specialist_name
        
class User(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=13)
    email = models.EmailField(blank = False, null = True)
    date = models.DateField(blank= True, null=True)
    from_time = models.TimeField()
    to_time = models.TimeField()
    specialist_name = models.ForeignKey(CustomUser, on_delete=models.CASCADE,)
    
    # @property
    # def lifespan(self):
    #     return '%s - present' % self.birthdate.strftime('%m/%d/%Y')
        

class Appointment_User(models.Model):
    name=models.CharField(max_length=50)
    phone=models.CharField(max_length=13)
    email=models.EmailField()
    password=models.CharField(max_length=10)  

    def __str__(self):
        return self.name 
    
    @staticmethod
    def get_appointment_user_by_email(email):
        try:
            return Appointment_User.objects.get(email=email)
        except:
            return False
