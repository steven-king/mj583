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
    path('student/(?P<pk>\d+)$', views.student),
    path('course/(?P<pk>\d+)$', views.course),

    path('admin/', admin.site.urls),
]

```
The regex expression says, match the letter P followed by a primary key <pk> that is a number \d for one or more places +. End of the line $.

6. Add a few imports to your views.py
```python
# jSchool/views.py
from django.shortcuts import render, get_object_or_404, redirect, render_to_response
```

