from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm , UserChangeForm , SetPasswordForm
from django import forms
from .models import Profile

class UpdateUserInfo(forms.ModelForm):

    phone=forms.CharField(label="",
        
        widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter your phone number'}),
        required=False
    )
    address1=forms.CharField(label="",
        
        widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter your primary address'}),
        required=False
    )
    address2=forms.CharField(label="",
        
        widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter your secondary address(optional)'}),
        required=False
    )
    city=forms.CharField(label="",
        
        widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter your city'}),
        required=False
    )
    state=forms.CharField(label="",
        
        widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter your state'}),
        required=False
    )
    zipcode=forms.CharField(label="",
        
        widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter your zipcode'}),
        required=False
    )
    country=forms.CharField(label="",
        
        widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter your country'}),
        required=False
    )

    class Meta:

        model = Profile
        fields = ['phone','address1','address2','city','state','zipcode','country']



class UpdatePasswordForm(SetPasswordForm):


    new_password1=forms.CharField(
        label="",
        max_length=20,
        widget=forms.PasswordInput(attrs={'class':'form-control','name':'password','type':'password','placeholder':'Enter your password'})
    )
    new_password2=forms.CharField(
        label="",
        max_length=20,
        widget=forms.PasswordInput(attrs={'class':'form-control','name':'password','type':'password','placeholder':'Enter your password again'})
    )



    class Meta:
        model=User
        fields=['new_password1','new_password2']



class UpdateUserForm(UserChangeForm):
    password=None
    first_name=forms.CharField(
        label="",
        max_length=40,
        widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter your first name'})
        ,required=False
    )


    last_name=forms.CharField(
        label="",
        max_length=40,
        widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter your last name'})
        ,required=False
    )

    email=forms.EmailField(
        label="",
        max_length=40,
        widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter your email address'})
        ,required=False
    
    )


    username=forms.CharField(
        label="",
        max_length=20,
        widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter your user name'})
        ,required=False
    
    )
    


    class Meta:

        model=User
        fields = ('first_name','last_name','email','username')

    








class SignUpForm(UserCreationForm):
    first_name=forms.CharField(
        label="",
        max_length=40,
        widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter your first name'})
    )


    last_name=forms.CharField(
        label="",
        max_length=40,
        widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter your last name'})
    )

    email=forms.EmailField(
        label="",
        max_length=40,
        widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter your email address'})
    )


    username=forms.CharField(
        label="",
        max_length=20,
        widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter your user name'})
    )
    password1=forms.CharField(
        label="",
        max_length=20,
        widget=forms.PasswordInput(attrs={'class':'form-control','name':'password','type':'password','placeholder':'Enter your password'})
    )
    password2=forms.CharField(
        label="",
        max_length=20,
        widget=forms.PasswordInput(attrs={'class':'form-control','name':'password','type':'password','placeholder':'Enter your password again'})
    )


    class Meta:

        model=User
        fields = ('first_name','last_name','email','username','password1','password2')

    
