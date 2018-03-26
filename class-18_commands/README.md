
# Start a Django app for nobel winners.

0. Build the image
```
docker build -t nobel-app .
```


1. Create a new virtual env if one is not created already:

```
docker run -v $PWD:/opt/project -it nobel-app python3 -m venv env
```

2. Install our requirements:

```
docker run -v $PWD:/opt/project -it nobel-app ./env/bin/pip3 install -r requirements.txt
```

3. To save time, I have already created most of the files needed including a project called nobel and an app called winners but if you were starting a django project from scratch you would do the following steps but for now, skip to part 8.

4. Start a new project called `nobel`:

```
docker run -v $PWD:/opt/project -it nobel-app ./env/bin/django-admin startproject nobel
```

5. Start a new app called `winners`:

```
docker run -v $PWD:/opt/project -it nobel-app ./env/bin/python3 nobel/manage.py startapp winners
```

6. Move the new application folder into our project folder:

```
mv winners nobel/nobel/
```

7. Create the models in `nobel/nobel/winners/models.py`

```python
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class Country(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


...
```

8. Add the app `nobel.winners` to `settings.INSTALLED_APPS` in `nobel/nobel/settings.py`:

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'nobel.winners',
]
```

9. To sync our database we are now going to use the Migrations Feature. Make migrations for our app:

```
docker run -v $PWD:/opt/project -it nobel-app ./env/bin/python3 nobel/manage.py makemigrations
```

10. Apply all migrations:

```
docker run -v $PWD:/opt/project -it nobel-app ./env/bin/python3 nobel/manage.py migrate
```

11. Add `nobel/nobel/winners/admin.py` so we can see our data in the admin:

```
from django.contrib import admin

from . import models

admin.site.register(models.Category)
admin.site.register(models.Country)
admin.site.register(models.Person)
admin.site.register(models.Winner)

```

12. Create a superuser so we can log in to the admin:

```
docker run -v $PWD:/opt/project -it nobel-app ./env/bin/python3 nobel/manage.py createsuperuser
```

13. Run the dev server (note the port flag used in the docker run command):

```
docker run -v $PWD:/opt/project -it -p 8000:8000 nobel-app ./env/bin/python3 nobel/manage.py runserver 0.0.0.0:8000
```

Go to the admin and you should see the admin page. Log in with the superuser
credentials you created.

--------------------------------------------------------------------------------

# Load the data using a custom management command

14. Make sure the the JSON file is in your working directory (the one with manage.py). We'll write a
management command to load this data in to our app.

```
mv ~/Downloads/wiki-clean.json .
```

15. In order to create a custom management command we have to create a specific
folder structure. It's documented well:

https://docs.djangoproject.com/en/2.0/howto/custom-management-commands/


16. STOP -- Let's start with understanding management commands. Now open management/commands/583_loader.py

17. Now. we will create a command `load_winners`  to load our JSON so we need to make a file in the
`management/commands/` directory called `load_winners.py`

18. This has been created for you but typically you would need to create the init files too. But for class we will skip to 19.
```
mkdir -p nobel/nobel/winners/management/commands
touch nobel/nobel/winners/management/__init__.py
touch nobel/nobel/winners/management/commands/__init__.py
touch nobel/nobel/winners/management/commands/load_winners.py
```

19. Now edit `load_winners.py` to load our data. See the example in the source.

20. Once the command is created you can run it with:

```
docker run -v $PWD:/opt/project -it nobel-app ./env/bin/python3 nobel/manage.py load_winners wiki-clean.json
```

21. If there were data errors you can inspect `skipped.json` (if it exists).


22. To DO list to make urls work for individual people
* Open url in urls.py
  must have reverse name
  
* new detail view
  needs to have access to person, winners models
  
* new template

* change href in list template
get_absolute_url

* models.py, add get_absolute_url function to the Winner class



22. After fixing the errors, you can run the command again but pass in the the skipped.json file.
```
docker run -v $PWD:/opt/project -it nobel-app ./env/bin/python3 nobel/manage.py load_winners wiki-clean.json
```

# Next, passing this data from Django to D3.JS!
