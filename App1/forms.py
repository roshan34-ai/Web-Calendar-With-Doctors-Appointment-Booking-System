from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.forms import AuthenticationForm
from django import forms
from .models import CustomUser, Appointment_User, User


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = '__all__'

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = '__all__'

class CustomAuthenticationForm(AuthenticationForm):

    class Meta:
        model = CustomUser
        fields = '__all__'

class RegistrationForm(CustomUserCreationForm):
    password1=forms.CharField(label="password", widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder' : '*******'}))
    password2=forms.CharField(label="Confirm Password", widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder': '*******'}))

    class Meta:
        model = CustomUser
        fields = ['specialist_name','email', 'phone', 'image', 'profession', 'locality', 'state_name', 'dist_name', 'experience', 'about', 'cunsultation_fees']
        labels = {'specialist_name':'Name', 'email':'Email', 'phone':'Phone', 'profession':'Profession', 'locality':'Locality', 'state_name':'State', 'dist_name':'District', 'experience':'Experience', 'about':'About', 'cunsultation_fees':'cunsultation_fees'}

        widgets = {
                 'specialist_name' : forms.TextInput(attrs={'class':'form-control', 'placeholder' : 'Enter Name Here'}),
                 'email' : forms.EmailInput(attrs={'class':'form-control', 'placeholder' : 'Enter Email Here', 'id':'email'}),
                 'phone' : forms.TextInput(attrs={'class':'form-control', 'placeholder' : 'Enter Phone Number Here'}),
                 'profession' : forms.TextInput(attrs={'class':'form-control'}),
                 'locality': forms.TextInput(attrs={'class':'form-control'}),
                 'state_name' : forms.TextInput(attrs={'class':'form-control'}),
                 'dist_name' : forms.TextInput(attrs={'class':'form-control'}),
                 'about' : forms.Textarea(attrs={'class':'form-control', 'id':'about', 'placeholder' : 'About'}),
                 'experience' : forms.TextInput(attrs={'class':'form-control', 'id':'experience', 'placeholder' : 'Your Experience'}),
                 'image' : forms.FileInput(attrs={'class':'form-control', 'accept':"image/png, image/jpg, image/jpeg, image/gif"}),
                 'cunsultation_fees': forms.TextInput(attrs={'class':'form-control'}),
        }





       