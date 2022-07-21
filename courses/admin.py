from django.contrib import admin

from courses.models import *

# Register your models here.
admin.site.register(Course)
admin.site.register(Material)
admin.site.register(Rating)
admin.site.register(CourseTeachers)
admin.site.register(CourseStudents)
