from django.contrib import admin
from .models import Student
from .models import Course

admin.site.register(Student)
admin.site.register(Course)
