from django.contrib import messages
from django.http.request import HttpRequest
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from courses import admin
from courses.models import Course, CourseTeachers, Material
from .forms import *
from .decorators import *


@admin_only
def manager_home_view(req):
    """
    Home view of administration section of the website
    """
    context = {}
    return render(req, 'manager/manager_home.html', context)


@admin_only
def manager_courses_view(req):
    courses = Course.objects.all()

    context = {'courses': courses}
    return render(req, 'manager/manager_courses.html', context)

@admin_only
def manager_users_view(req):
    users = User.objects.all()

    context = {'users': users}
    return render(req, 'manager/manager_users.html', context)

@admin_only
def manager_user_edit_view(req, username):
    user = get_object_or_404(User, username=username)
    return render(req, 'manager/user_info.html', {'user': user})

@admin_only 
def user_delete_endpoint(req, username):
    user = get_object_or_404(User, username=username)
    user.delete()
    return redirect('manager_user')

@admin_only 
def user_active_flip_endpoint(req, username):
    user = get_object_or_404(User, username=username)
    user.is_active = not user.is_active
    user.save()
    return redirect('manager_user')

@admin_only
def course_create_view(req):
    """
    Create a new course
    """
    if req.method == 'GET':
        form = CourseDetailsForm()
        context = {'action': 'Tạo mới', 'form': form}
        return render(req, 'courses/create_edit.html', context)
    if req.method == 'POST':
        print("POST received")
        form = CourseDetailsForm(req.POST, req.FILES)
        if form.is_valid():
            course = form.save(commit=False)
            course.cover_image_binary = form.cleaned_data['cover_image'].file.read()
            course.save()
            messages.success(req, 'Khóa học đã được tạo: %s' % course.name)
            print('New course created')
            return redirect('course_create')
        else:
            print(form.errors)
            print('Form invalid!')
        return redirect('course_create')


@admin_only
def course_edit_view(req, course_id):
    course = Course.objects.get(id=course_id)
    form = CourseDetailsForm(instance=course)
    if req.method == 'GET':
        context = {'form': form, 'action': 'Chỉnh sửa thông tin'}
        return render(req, 'courses/create_edit.html', context)
    else:
        form = CourseDetailsForm(req.POST, req.FILES, instance=course)
        if form.is_valid():
            course = form.save(commit=False)
            if form.cleaned_data['cover_image']:
                try:
                    course.cover_image_binary = form.cleaned_data['cover_image'].file.read()
                except FileNotFoundError:
                    pass
            course.save()
            messages.success(req, 'Khóa học đã được sửa: %s' % course.name)
            print("Course saved!")
            return redirect('manager_course')
        else:
            print("Form invalid!")
        return redirect('home')


@admin_only
def course_delete_view(req: HttpRequest, course_id):
    course = get_object_or_404(Course, id=course_id)

    if req.method == 'GET':
        context = {'course': course}
        return render(req, 'courses/delete.html', context)
    elif req.method == 'POST':
        course_name = course.name
        course.delete()
        messages.success(req, "Khóa học đã được xóa: %s" % course_name)
        return redirect('manager_course')


@admin_only
def teacher_approve_list_view(req: HttpRequest):
    """
    Show a list of teachers waiting for approval
    """
    waiting_teachers = UserProfile.get_all_waiting_teachers()
    if req.method == 'POST':
        teacher_username = req.POST.get('teacher_username')
        teacher_instance = get_object_or_404(User, username=teacher_username)
        teacher_name = str(teacher_instance.last_name + teacher_instance.first_name)

        if 'req_approve' in req.POST:
            teacher_instance.is_active = True
            teacher_instance.save()
            messages.success(req, 'Đã xét duyệt giáo viên: %s' % teacher_name)
            # TODO: send notification email
        elif 'req_disaprv' in req.POST:
            teacher_instance.delete()
            messages.success(req, 'Đã từ chối giáo viên: %s' % teacher_name)
            # TODO: send notification email
        else:
            return render(req, 'home/error.html',
                          {'error_message': 'Chúng tôi không thể xử lý yêu cầu này. '
                                            'Vui lòng liên hệ đội ngũ phát triển phần mềm.'})

    context = {'waiting_teachers': waiting_teachers}
    return render(req, 'manager/teacher_approve_list.html', context)

@admin_only
def teacher_assign_view(req: HttpRequest, course_id):
    course = get_object_or_404(Course, id=course_id)
    
    if req.method == 'POST':
        form = AssignTeacherForm(req.POST)
        if form.is_valid():
            form.save()

    course_teacher = CourseTeachers.objects.filter(course=course)
    form = AssignTeacherForm(initial={'course': course})

    ctx = {'course_teachers': course_teacher, 'form': form, 'course': course}
    return render(req, 'manager/teacher_assign.html', ctx)

@admin_only
def teacher_deassign_view(req: HttpRequest, course_id, username):
    if req.method == 'POST':
        entry = get_object_or_404(CourseTeachers, course__id=course_id, teacher__username=username)
        entry.delete()
        return redirect(reverse('assng_teacher_course', kwargs={'course_id': course_id}))
    else:
        return render(req, 'home/error.html', {'error_message': 'Lỗi hệ thống! Endpoint này không hỗ trợ GET.\nVui lòng liên hệ nhà phát triển.'})