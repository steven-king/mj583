# Output the clean wiki data

Run the notebook server from class 10

```
docker run -p 9000:9000 uncdataviz/class-10:pandas-cleaning
```

Go to 127.0.0.1:9000 and export the cleaned data to JSON. See
`Cleaning Wiki Dates & Save To JSON.ipynb`

The export command should be:

```
df.to_json("wiki-clean.json", orient="records")
```

The 2nd argument is the "orientation" of the output data. By using the `records`
format we will get a list containing each record instead of a mapping of columns
and their data.

Consider a dataframe with the following contents:

```
d = pd.DataFrame([{"col_a":"some value", "col_b":"another value"}])
```

Which looks like:

```
        col_a          col_b
0  some value  another value
```

Now compare the default orientation with the `records` orientation:

```
print(d.to_json())

>>> {"col_a":{"0":"some value"},"col_b":{"0":"another value"}}

print(d.to_json(orient="records"))
>>> [{"col_a":"some value","col_b":"another value"}]
```

Go to the home page of the notebook server and download the JSON.

--------------------------------------------------------------------------------

# Start a Django app for nobel winners.

Create a new virtual env if one is not created already:

```
docker run -v $PWD:/opt/project -it nobel-app python3 -m venv env
```

Install our requirements:

```
docker run -v $PWD:/opt/project -it nobel-app ./env/bin/pip3 install -r requirements.txt
```

Start a new project called `nobel`:

```
docker run -v $PWD:/opt/project -it nobel-app ./env/bin/django-admin startproject nobel
```

Start a new app called `winners`:

```
docker run -v $PWD:/opt/project -it nobel-app ./env/bin/python3 nobel/manage.py startapp winners
```

Move the new application folder into our project folder:

```
mv winners nobel/nobel/
```

Create the models in `nobel/nobel/winners/models.py`

```
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)


class Country(models.Model):
    name = models.CharField(max_length=100)


class Winner(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, "CASCADE")
    country = models.ForeignKey(Country, "CASCADE")
    year = models.PositiveIntegerField()

```

Add the app `nobel.winners` to `settings.INSTALLED_APPS` in `nobel/nobel/settings.py`:

```
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

Make migrations for our app:

```
docker run -v $PWD:/opt/project -it nobel-app ./env/bin/python3 nobel/manage.py makemigrations
```

Apply all migrations:

```
docker run -v $PWD:/opt/project -it nobel-app ./env/bin/python3 nobel/manage.py migrate
```

Add `nobel/nobel/winners/admin.py` so we can see our data in the admin:

```
from django.contrib import admin

from . import models

admin.site.register(models.Category)
admin.site.register(models.Country)
admin.site.register(models.Person)
admin.site.register(models.Winner)

```

Create a superuser so we can log in to the admin:

```
docker run -v $PWD:/opt/project -it nobel-app ./env/bin/python3 nobel/manage.py createsuperuser
```

Run the dev server (note the port flag used in the docker run command):

```
docker run -v $PWD:/opt/project -it -p 8000:8000 nobel-app ./env/bin/python3 nobel/manage.py runserver 0.0.0.0:8000
```

Go to the admin and you should see the admin page. Log in with the superuser
credentials you created.

--------------------------------------------------------------------------------

# Load the data using a custom management command

Copy over the JSON you downloaded to your working directory. We'll write a
management command to load this data in to our app.

```
mv ~/Downloads/wiki-clean.json .
```

In order to create a custom management command we have to create a specific
folder structure. It's documented well:

https://docs.djangoproject.com/en/2.0/howto/custom-management-commands/

We will create a command `load_winners` so we need to make a file in the
`management/commands/` directory called `load_winners.py`

```
mkdir -p nobel/nobel/winners/management/commands
touch nobel/nobel/winners/management/__init__.py
touch nobel/nobel/winners/management/commands/__init__.py
touch nobel/nobel/winners/management/commands/load_winners.py
```

Now edit `load_winners.py` to load our data. See the example in the source.

Once the command is created you can run it with:

```
docker run -v $PWD:/opt/project -it nobel-app ./env/bin/python3 nobel/manage.py load_winners wiki-clean.json
```

If there were data errors you can inspect `skipped.json` (if it exists).
