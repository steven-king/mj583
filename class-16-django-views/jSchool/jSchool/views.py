#jSchool/views.py

from django.shortcuts import render
from jSchool.models import Course, Student

def home(request):
    context = {
        'student_count': Student.objects.count(),
        'course_count': Course.objects.count(),
    }
    return render(request, "home.html", context)


def courses(request):
    context = {
        course_list : Course.objects.all()
    }
    return render(request, "courses.html", context)

def course(request):
    context = {

    }
    return render(request, "course.html", context)

def students(request):
    context = {

    }
    return render(request, "students.html", context)

def student(request):
    context = {

    }
    return render(request, "student.html", context)
