Today we are going to work on modeling data with a simple concept and loading some sample data.

1. Pull the latest image from docker
``` docker pull steventking/django-starter-sqlite:latest ```

This includes an installed version of djanog2 and sqlite

2. Now we will create an alias to run things so we dont have to type this long command:
```
#don't rune this
docker run -v $PWD:/opt/project -it class-14 python3

```
#run this to create an alisis

alias run_d="docker run -v $PWD:/opt/project -it steventking/django-starter-sqlite"
```
Now you can run any command using
```
run_d projectname/manage.py
```

