## Preparing Django for Deployment

Django Prep
  - Debug = False
  - Collet Static
  - Whitenoise

Deployment
  - Docker Image
  - Digital Ocean
  - SSH Keys
  - Push Image
  - Run Container

Here is a video by @leetrout that walks through all of this:
https://www.youtube.com/watch?v=plAGgfSCwf4&feature=youtu.be

0.1 Review Docker command
```
docker run -v $PWD:/opt/project -it -p 8000:8000 nobel-app ./env/bin/python3 nobel/manage.py runserver 0.0.0.0:8000
```
```python
application command copyVolumn from:to interactiveTerminal port from:to containerName usingEnv runFilePath command
```
Check it at http://localhost:8000/

0.2 Review BASE_DIR concept in django
```python
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
```


1. Turn off Debug
Change DEBBUG var to False
```python
# nobel/nobel/settings.py
## Change Line 25 and 26

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

```

2. Set ALLOWED_HOSTS
NOTE: This is not secure or ideal and should be explicit but for now we are doing to allow all hosts.
```python
ALLOWED_HOSTS = ['*']
```
Run and test server and note css, js and images don't work because Django does not like to serve static files.

3. Prepare Static Files
https://docs.djangoproject.com/en/2.0/ref/contrib/staticfiles/#module-django.contrib.staticfiles

```python
# nobel/nobel/settings.py
## end of file
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
```

4. Run collect static
Run the command that looks for all files in the STATIC_URL and copies them to the STATIC_ROOT
```
docker run -v $PWD:/opt/project -it -p 8000:8000 nobel-app ./env/bin/python3 nobel/manage.py collectstatic
```

After complete, ls the static folder now in this current directory.
This is used for security purposes so we can seperate application code (python) from static raw files.
If you re-run server, it will not work.

5. We are going to use python app called Whitenoise to serve these files.
http://whitenoise.evans.io/en/stable/
Open requirements.txt and add whitenoise to the list so it reads.
```
django==2.0
requests
whitenoise
```
Then you need to install it using pip install.
```
docker run -v $PWD:/opt/project -it -p 8000:8000 nobel-app ./env/bin/pip3 install -r requirements.txt
```

White noise docs explains how to use with Django!!!!
Docs say,

"Edit your settings.py file and add WhiteNoise to the MIDDLEWARE_CLASSES list, above all other middleware apart from Django’s SecurityMiddleware:""


```python
MIDDLEWARE_CLASSES = [
  # 'django.middleware.security.SecurityMiddleware',
  'whitenoise.middleware.WhiteNoiseMiddleware',
  # ...
]
```

6. Now run and test!
```
docker run -v $PWD:/opt/project -it -p 8000:8000 nobel-app ./env/bin/python3 nobel/manage.py runserver 0.0.0.0:8000
```
All should work.
