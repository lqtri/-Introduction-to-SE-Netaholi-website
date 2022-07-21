from django.urls import path
from . import views

urlpatterns = [
    path('search', views.search_view, name='course_search'),
    path('mycourses', views.my_courses_view, name='my_courses'),
    path('<str:course_id>/details', views.detail_page_view, name='details'),
    path('<str:course_id>/enroll', views.enroll_view, name='enroll'),
    path('<str:course_id>/dashboard', views.dashboard_view, name='dashboard'),
    path('<str:course_id>/lesson', views.lesson_view, name='lesson'),
    path('<str:course_id>/material/create', views.material_create_view, name='material_create'),
    path('<str:course_id>/material/<str:material_id>', views.material_view, name='material'),
    path('<str:course_id>/material/edit/<str:material_id>', views.material_create_edit, name='material_edit'),
    path('<str:course_id>/rate', views.rating_view, name='course_rate'),
]
