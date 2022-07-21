from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import fields, widgets
from courses.models import Course, CourseTeachers

class CourseDetailsForm(forms.ModelForm):
    """
    Form for edit or create a new course
    """
    class Meta:
        model = Course
        fields = '__all__'

class AssignTeacherForm(forms.ModelForm):
    """
    Form for assigning a teacher to a course
    """
    teacher = forms.ModelChoiceField(
        queryset=User.objects.filter(userprofile__is_teacher=True),
        widget=forms.Select
    )

    class Meta:
        model = CourseTeachers
        fields = '__all__'
        widgets = {
            'course': forms.HiddenInput()
        }
        