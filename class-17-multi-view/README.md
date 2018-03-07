## Creating Multiple views into the data ##

### Better Alias ###
Previously, we have been making an alias for each termnal session. But since we have done it twice, we should save us the effort and save it to our bash profile so we can use it forever!

1. Open your bash profile file.
```
vim ~/.bashrc
```

2. Insert the text below by using the key i to insert.
```
alias drm="docker run -v $PWD:/opt/project -p 8000:8000 -it steventking/django-starter-sqlite ./env/bin/python3 jSchool/manage.py"
```

3. Save and Quit.
Press escape to exit out of Insert Mode, colon to enter a command, w to write and q to quit.
```
:wq
```

4. You can restart the terminal app or you can use this command to reload the bash profile. 
```
source ~/.bashrc
```

## Individual Record templates ##

5. We need to enable the urls for /student/1234 but we need it for every student and the same for every course. ex. course/1/.
```python
urlpatterns = [
    path('', views.home),
    path('course/<int:pk>', views.course),

    path('admin/', admin.site.urls),
]

```

6. Add a few imports to your views.py and then handle receiving the primary key from the url.
```python
# jSchool/views.py
from django.shortcuts import render, get_object_or_404, redirect, render_to_response
...

def course(request, pk):
    course = get_object_or_404(Course, id=pk)
    context = {
        #course = Course.objects.order_by('?'[0])
        'course' : course,
    }
    return render(request, "course.html", context)

```
7. Edit the course.html template to receive the data using template tags. 
```html
{% extends "base.html" %}
{% load humanize %}
{% block content %}
<h2>Course: {{ course.name }}</h2>
<p>Details</p>
<ul>
    <li>{{ course.instructor }}</li>
    <li>{{ course.term }}</li>

</ul>
{% endblock %}


```


What is happening?

a. A request is sent with the primary ky in the url (defination of the function)

b. if it does not exsist, give a 404 error.

c. pass the entire model data to the template as a context variable.


8. Now lets repeat to make the student pages work, 

```python 
#jSchool/urls.py
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('course/<int:pk>', views.course),
    path('student/<int:pk>', views.student),

    path('admin/', admin.site.urls),
]

```

```python 
#jSchool/views.py
...
def student(request, pk):
    student = get_object_or_404(Student, id=pk)
    context = {
        'student' : student,
    }
    return render(request, "student.html", context)

```

```html
<!-- student.html
{% extends "base.html" %}
{% load humanize %}
{% block content %}
<h2>{{ student.name }}</h2>
<p>Student Details</p>
<ul>
    <li>PID: {{ student.pid }}</li>
    <li>Current Grade: {{ student.grade }}</li>

</ul>
{% endblock %}

```

### Listing All the students and courses ###

9. Start by adding all the urls.
```python
urlpatterns = [
    path('', views.home),
    path('courses', views.course_list),
    path('students', views.student_list),
    path('course/<int:pk>', views.course),
    path('student/<int:pk>', views.student),

    path('admin/', admin.site.urls),
]

```

10. Continue by selecting all of you courses in the view for course_list.
```python
def course_list(request):
    course_list = Course.objects.all()
    context = {
        'course_list' : course_list
    }
    return render(request, "course_list.html", context)

```
11. Create a course_list.html in the templates folder and add this code.
```html
{% extends "base.html" %}
{% load humanize %}
{% block content %}
<h2>{{ course.name }}</h2>
<p>Course Details</p>
<ul>
    <li>Instructor: {{ course.instructor }}</li>
    <li>Semester: {{ course.term }}</li>

</ul>
{% endblock %}

```

12. But what about the 5000 students????
A quick google church for djanogo pagination answer the qustion. 

13. On the views.py, you will add this line ```from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger```
so the header looks like this:
```python
from django.shortcuts import render, get_object_or_404, redirect, render_to_response
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from jSchool.models import Course, Student

```
Then update the student_list view to include the pagination code.
```python
...
def student_list(request):
    student_list =  Student.objects.all()
    paginator = Paginator(student_list, 25) # Show 25 contacts per page
    page = request.GET.get('page')
    students = paginator.get_page(page)
    context = {
        'students' : students
    }
    return render(request, "student_list.html", context)

...

```

14. Create a student_list.html file in the templates folder and use this code:
```html
{% extends "base.html" %}

{% block content %}
<ul>
{% for student in students %}
    {# Each "student" is a Student model object. #}

    <li><a href="{{ student.id }}">{{ student.name }}</a></li>
{% endfor %}
</ul>
<div class="pagination">
    <span class="step-links">
        {% if contacts.has_previous %}
            <a href="?page=1">&laquo; first</a>
            <a href="?page={{ students.previous_page_number }}">previous</a>
        {% endif %}

        <span class="current">
            Page {{ students.number }} of {{ students.paginator.num_pages }}.
        </span>

        {% if contacts.has_next %}
            <a href="?page={{ students.next_page_number }}">next</a>
            <a href="?page={{ students.paginator.num_pages }}">last &raquo;</a>
        {% endif %}
    </span>
</div>

```

