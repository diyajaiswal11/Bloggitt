from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Comment, Profile, Post

class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=100)

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'email')


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'username',  
            'email', 
        ]

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'profile_image'
        ]

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'body')
        
        widgets={

            'name':forms.TextInput(attrs={'class' : 'form-control'}),
            'body':forms.Textarea(attrs={'class' : 'form-control'})

        }