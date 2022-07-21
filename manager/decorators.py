from django.http import HttpResponse
from django.http.response import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from courses.models import Course
from home.models import UserProfile


def admin_only(view_func):
    def wrapper(req, *args, **kwargs):
        current_user = req.user

        if current_user.is_staff:
            return view_func(req, *args, **kwargs)
        else:
            return render(req, 'home/error.html', {'error_message': 'Bạn không thể truy cập vào trang quản trị!!!'})
    return login_only(wrapper)


def login_only(view_func):
    def wrapper(req, *args, **kwargs):
        return view_func(req, *args, **kwargs)
    return login_required(function=wrapper, login_url='login')


def teacher_admin_only(view_func):
    def wrapper(req, *args, **kwargs):
        current_user = req.user
    
        if current_user.is_staff or current_user.userprofile.is_teacher:
            return view_func(req, *args, **kwargs)
        else:
            return render(req, 'home/error.html', {'error_message': 'Chỉ có giảng viên hoặc quản trị viên mới có thể sử dụng tính năng này!'})
    return login_only(wrapper)

def course_expire_check(view_func):
    def wrapper(req, course_id, *args, **kwargs):
        course = get_object_or_404(Course, id=course_id)
        if course.is_ended:
            return render(req, 'home/error.html', {'error_message': 'Bạn không thể truy cập tính năng này do khóa học đã hết thời hạn.'})
        else:
            return view_func(req, course_id, *args, **kwargs)
    return wrapper