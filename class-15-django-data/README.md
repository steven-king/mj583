Today we are going to work on modeling data with a simple concept and loading some sample data.

## Set Up Django, Easier ##
1. Pull the latest image from docker
``` docker pull steventking/django-starter-sqlite:latest ```

This includes an installed version of djanog2 and sqlite

2. Create the virtual env to run in
```
docker run -v $PWD:/opt/project -it steventking/django-starter-sqlite python3 -m venv env
```

3. Install Django
```
docker run -v $PWD:/opt/project -it steventking/django-starter-sqlite ./env/bin/pip3 install -r requirements.txt
```
4. Starte a Django Project
```
docker run -v $PWD:/opt/project -it steventking/django-starter-sqlite ./env/bin/django-admin startproject jSchool
```

5. Run Django Server
```
docker run -v $PWD:/opt/project -p 8000:8000 -it steventking/django-starter-sqlite ./env/bin/python3 jSchool/manage.py runserver 0.0.0.0:8000

```
6. Now we will create an alias to run things so we dont have to type this long command:
```
#don't run this
docker run -v $PWD:/opt/project -p 8000:8000 -it steventking/django-starter-sqlite ./env/bin/python3 jSchool/manage.py

```
```
#run this to create an alisis

alias drm="docker run -v $PWD:/opt/project -p 8000:8000 -it steventking/django-starter-sqlite ./env/bin/python3 jSchool/manage.py"
```
Now you can run any command using

```
drm runserver 0.0.0.0:8000 
or
drm any-django-manage-command [params]
```
## Build App ##
7. Make Models for Students by creating a models.py in the app folder.

```python
#path: jSchool/jSchool
from django.db import models

class Student(models.Model):
    name = models.CharField(unique=True, max_length=50)
    pid = models.CharField(unique=True, max_length=12)
    grade = models.IntegerField(unique=False)


#note: the name field should not be unique but this is to demenstrate an error and how to handle it with real data.
#note2: grade field should have null=True, this is for demo purpose. 


```
8. Build model for Course
```python
# same models.py, below the first model.
class Course(models.Model):
    name = models.CharField(max_length=50)
    call_number = models.CharField(unique=False, max_length=4)
    instructor = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    term = models.CharField(max_length=200)
    date = models.DateField()
    
```

9. Change the settings.py to include your app
```python

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'jSchool',
]
```

10. Note, you are making a lot of changes. Make sure you watch your syntax!

11. Test to see if you broke something. Run the server.
```
drm runserver 0.0.0.0:8000
```
Potential Errors:
table does not exsist: 
We must sync the models with the database.

12. Now we need to build or sync the datbase to reflect the models.
```
drm migrate --run-syncdb
```

13. Now try again.
```
drm runserver 0.0.0.0:8000
```

14. Create a login superuser so you can see the admin tool.

```
drm createsuperuser

# leave blank or give it a username. Be consistant, you will do this a lot.
# leave email blank, 
# Required strong password of 8+ characters
```

15. Login to the admin tool at 
http://localhost:8000/admin

Use the user and password you just created.
Note what is avaialable in the admin tool. Where are our models?

16. Create an admin.py to enable editing of the data in the admin tool.
```python
#jSchool/jSchool/admin.py

from django.contrib import admin
from .models import Student
from .models import Course

admin.site.register(Student)
admin.site.register(Course)

```

17. Restart.
```
drm runserver 0.0.0.0:8000
```
Login to the admin tool at 
http://localhost:8000/admin
Note what is avaialable in the admin tool. Models are there now but no data.

## Loading Data ##
This is going to be a process you will do over and over. I have provided you some sample JSON files so you can load them over and over. Note, I have made a mistake in the Courses JSON so you can see what happens with bad json.

18. You will Sync the db (if not already done), then load to different json files.

```

# to sync the database
drm migrate --run-syncdb

# to load the courses data
drm loaddata data_class.json
#note, error in json, remove the last comma, save and rerun the command.

# to load the student data
drm loaddata data_students_withgrad.json


```

Now test
```
drm runserver 0.0.0.0:8000
```
Login to the admin tool at 
http://localhost:8000/admin
You should have data!

19. But it does not look great, lets do some changes to the models.
```python
#jSchool/jSchool/models.py

... after student model ...
class Meta(object):
            ordering = ('pid', 'name')

    def __str__(self):
        return U'%s %s' %(self.name, self.pid)
        
        
        
... after course model ...
class Meta(object):
        verbose_name_plural = "Courses"
        ordering = ('-date', 'name')

    def __str__(self):
        return U'%s %s' %(self.call_number, self.name)

    def save(self, *args, **kwargs):
        self.name = self.name.upper()
        super(Course, self).save(*args, **kwargs)

```
See final models.py in this repo.

20. Making data changes.
As you make changes to your models.py, you will have to repeate a few steps. I might havge dont this 11-15 times while preparing.

A. Kill/Dump/Delete the database
``` 
rm jSchool/db.sqlite3
```

B. Sync or Rebuild the database
```
# to sync the database
drm migrate --run-syncdb
```
C. Load new data (in this case, twice)
```
# to load the courses data
drm loaddata data_class.json
#note, error in json, remove the last comma, save and rerun the command.

# to load the student data
drm loaddata data_students_withgrad.json
```
D. create super user
```
drm createsuperuser
```
E. Run Server
```
drm runserver 0.0.0.0:8000
```
Login to the admin tool at 
http://localhost:8000/admin
You should see the changes!

