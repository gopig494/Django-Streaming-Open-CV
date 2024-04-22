from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from streaming.models import *

class SignUpForm(forms.Form):
    first_name = forms.CharField(max_length=20)
    last_name = forms.CharField(max_length=20)
    user_name = forms.CharField(max_length=20)
    email = forms.EmailField()
    password = forms.CharField(max_length=20,widget=forms.PasswordInput)
    confirm_password = forms.CharField(max_length=20,widget=forms.PasswordInput)

    def clean(self):
        """ Method to validata form values. """
        cleaned_data = super().clean()
        if cleaned_data.get('password') and cleaned_data.get('confirm_password'):
            if cleaned_data.get('password') != cleaned_data.get('confirm_password'):
                # self.add_error('confirm_password', 'Passwords must match.')
                raise forms.ValidationError("The passwords do not match. Please try again.")
        exe_username = User.objects.filter(username = cleaned_data.get("user_name")).exists()
        if exe_username:
            raise forms.ValidationError("User name already taken.Please try different user name.")    
        email = User.objects.filter(email = cleaned_data.get("email")).exists()
        if email:
            raise forms.ValidationError("E-mail is already exists.Please try different email.")    
        return cleaned_data

class LogInForm(forms.Form):
    user_name = forms.CharField(max_length=30,label="User name or email")
    password = forms.CharField(max_length=30,widget=forms.PasswordInput)

    def clean(self):
        """ Method to validata form values. """
        cleaned_data = super().clean()
        auth = authenticate(username = cleaned_data.get('user_name'),password = cleaned_data.get('password'))  
        if not auth:
            raise forms.ValidationError("Invalid username or password.")
        else:
            self.auth_info = auth
        return cleaned_data

class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ('name', 'video_url')
        labels = {
            'name': 'Video Title'
        }

    # def clean_video_url(self):
    #     video_url = self.cleaned_data['video_url']
    #     if not video_url.startswith('http'):
    #         raise forms.ValidationError('The video URL must start with "http"')
    #     return video_url
