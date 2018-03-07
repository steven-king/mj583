"""jSchool URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('courses/', views.course_list, name='jSchool_course_list'),
    path('students/', views.student_list, name='jSchool_student_list'),
    path('course/<int:pk>', views.course, name='jSchool_course'),
    path('student/<int:pk>', views.student, name='jSchool_student'),

    path('admin/', admin.site.urls),
]
