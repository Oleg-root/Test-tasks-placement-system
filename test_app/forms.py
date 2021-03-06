from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Solution, Notification, Response


class UploadFileForm(forms.Form):
    file = forms.FileField()

class ResponseForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = ['content']