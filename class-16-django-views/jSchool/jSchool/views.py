#jSchool/views.py

from django.shortcuts import render, get_object_or_404, redirect, render_to_response
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from jSchool.models import Course, Student

def home(request):
    context = {
        'student_count': Student.objects.count(),
        'course_count': Course.objects.count(),
    }
    return render(request, "home.html", context)


def course_list(request):
    course_list = Course.objects.all()
    context = {
        'course_list' : course_list
    }
    return render(request, "course_list.html", context)

def course(request, pk):
    course = get_object_or_404(Course, id=pk)
    context = {
        #course = Course.objects.order_by('?'[0])
        'course' : course,
    }
    return render(request, "course.html", context)

def student_list(request):
    student_list =  Student.objects.all()
    paginator = Paginator(student_list, 25) # Show 25 contacts per page
    page = request.GET.get('page')
    students = paginator.get_page(page)
    context = {
        'students' : students
    }
    return render(request, "student_list.html", context)

def student(request, pk):
    student = get_object_or_404(Student, id=pk)
    context = {
        #course = Course.objects.order_by('?'[0])
        'student' : student,
    }
    return render(request, "student.html", context)
