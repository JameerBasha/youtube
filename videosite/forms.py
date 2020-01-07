from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class VideoUploadForm(forms.Form):
    title = forms.CharField(label='Title', max_length=200)
    file_data = forms.FileField()
    categories = forms.CharField(label='Categories', max_length=1000)


class CommentForm(forms.Form):
    comment = forms.CharField(label='Comment', max_length=1000)
