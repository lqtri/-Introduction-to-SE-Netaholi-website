from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import fields, widgets
from .models import MAX_LENGTH_LONG, MAX_LENGTH_MED, Course, Material, Rating


class MaterialForm(forms.ModelForm):
    """
    Form for edit or create a new course material
    """
    class Meta:
        model = Material
        fields = ('title', 'content', 'type')

class RatingForm(forms.ModelForm):
    """
    Form for rating a course
    """
    class Meta:
        model = Rating
        fields = ('star', 'content')
        widgets = {
            'star': forms.HiddenInput(),
            'content': forms.Textarea()
        }
