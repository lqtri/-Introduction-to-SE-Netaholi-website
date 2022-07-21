from django.urls import path
from . import views

urlpatterns = [
    path('', views.manager_home_view, name='manager_home'),
    path('courses', views.manager_courses_view, name='manager_course'),
    path('users', views.manager_users_view, name='manager_user'),
    path('users/<str:username>', views.manager_user_edit_view, name='user_info'),
    path('users/del/<str:username>', views.user_delete_endpoint, name='user_delete'),
    path('users/activ/<str:username>', views.user_active_flip_endpoint, name='user_active_flip'),
    path('create/course', views.course_create_view, name='course_create'),
    path('edit/course/<str:course_id>', views.course_edit_view, name='course_edit'),
    path('delete/course/<str:course_id>', views.course_delete_view, name='course_delete'),
    path('tchrapprove', views.teacher_approve_list_view, name='aprv_teacher_list'),
    path('tchrassgn/<str:course_id>', views.teacher_assign_view, name='assng_teacher_course'),
    path('tchrdassgn/delete/<str:course_id>/<str:username>', 
        views.teacher_deassign_view,
        name='deassng_teacher_course'
    ),
]
