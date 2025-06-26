from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import MembershipApplication, Profile, Post, Comment

class MembershipApplicationForm(forms.ModelForm):
    class Meta:
        model = MembershipApplication
        fields = ['name', 'school', 'classroom']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input'}),
            'school': forms.TextInput(attrs={'class': 'form-input'}),
            'classroom': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. Primary 3A'}),
        }

class UserLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-input'}))

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['school', 'classroom', 'bio']
        widgets = {
            'school': forms.TextInput(attrs={'class': 'form-input'}),
            'classroom': forms.TextInput(attrs={'class': 'form-input'}),
            'bio': forms.Textarea(attrs={'class': 'form-input', 'rows': 4}),
        }

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-input', 'rows': 3, 'placeholder': 'Share what\'s happening at school...'}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-input', 'rows': 2, 'placeholder': 'Add a comment...'}),
        }

class ApproveApplicationForm(forms.Form):
    username = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'form-input', 'type': 'password'}))