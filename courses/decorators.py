from django.contrib.auth.models import User, Group
from .models import CourseStudents, CourseTeachers, Course
from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponse, HttpRequest


def enrolled_only(view_func):
    def wrapper(req: HttpRequest, course_id, *args, **kwargs):
        # Get course
        course = get_object_or_404(Course, id=course_id)
        # Check if user is enrolled in course (admins are granted access by default)
        user = req.user
        if user.is_staff or course.is_enrolled(user.username):
            return view_func(req, course_id, *args, **kwargs)
        return render(req, 'home/error.html', {'error_message': 'Bạn chưa đăng ký khóa học này!'})
    return wrapper
