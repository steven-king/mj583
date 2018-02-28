Today we are going to work on modeling data with a simple concept and loading some sample data.

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
X. Now we will create an alias to run things so we dont have to type this long command:
```
#don't run this
docker run -v $PWD:/opt/project -p 8000:8000 -it steventking/django-starter-sqlite ./env/bin/python3 jSchool/manage.py

```
```
#run this to create an alisis

alias docker-manage-py="docker run -v $PWD:/opt/project -p 8000:8000 -it steventking/django-starter-sqlite ./env/bin/python3 jSchool/manage.py"
```
Now you can run any command using

```
run_d projectname/manage.py
```

