## Adding Views and Templates

### Remember, three files required ###
1. Open the url on urls.py
2. Add the View and context on views.py
3. Edit the template in the app/template directory

1. Make sure you are working the the class 15 (last week's folder). We will just keep adding to this. 
Note: All of the finished code is in this repo for your refrence.

2. Make sure your alais is working and your server works.
```
runserver 0.0.0.0:8000 
```

If the alisis does not work, run 
```
alias drm="docker run -v $PWD:/opt/project -p 8000:8000 -it steventking/django-starter-sqlite ./env/bin/python3 jSchool/manage.py"

```

3. Add a new ur called test/ to tue url.py inside the jSchool App folder
```python
#jschool/urls.py
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('test/', views.home),
    path('admin/', admin.site.urls),
]

```

4. Create a views.py file in your jSchool app directory. 
```python

#jSchool/views.py

from django.shortcuts import render
from jSchool.models import Course, Student

def home(request):
    context = {
        'student_count': Student.objects.count(),
        'course_count': Course.objects.count(),
    }
    return render(request, "base.html", context)

```



5. Create a templates folder inside the jSchool App
6. Create a new html file called base.html inside the templates folder.

```html
<!-- jSchool/templates/base.html -->
<html lang="en">
<head>
  <meta charset="utf-8">

  <title>UNC Interactive Media</title>
  <meta name="description" content="Learning Django">

  <link rel="stylesheet" href="css/styles.css?v=1.0">

</head>

<body>
  <script src="js/scripts.js"></script>
  <h1> UNC Interactive Media</h1>
  <h2>Students and Courses</h2>
  <p>This new interactive media major has {{student_count}} students taking {{ course_count}} courses.
</body>
</html>
```

7. Run the server and test!
```
drm runserver 0.0.0.0:8000 



