# Class 12 - Django & Postgres

<!-- TOC -->

- [Class 12 - Django & Postgres](#markdown-header-class-12-django-postgres)
    - [Terms](#markdown-header-terms)
    - [New Concepts](#markdown-header-new-concepts)
        - [Docker volumes](#markdown-header-docker-volumes)
        - [Docker container names](#markdown-header-docker-container-names)
        - [Ubuntu](#markdown-header-ubuntu)
        - [Postgres](#markdown-header-postgres)
        - [Postico](#markdown-header-postico)
    - [Instructions](#markdown-header-instructions)
        - [Build the base image](#markdown-header-build-the-base-image)
        - [Copy in the requirements & install in a virtualenv](#markdown-header-copy-in-the-requirements-install-in-a-virtualenv)
            - [Breakdown](#markdown-header-breakdown)
            - [Recap](#markdown-header-recap)
        - [Create & install requirements.txt](#markdown-header-create-install-requirementstxt)
        - [Create a sample django project](#markdown-header-create-a-sample-django-project)
        - [Run the sample server](#markdown-header-run-the-sample-server)
    - [Postgres](#markdown-header-postgres_1)
        - [Switch to postgres](#markdown-header-switch-to-postgres)
        - [Run postgres](#markdown-header-run-postgres)
        - [Launch Postico](#markdown-header-launch-postico)
        - [Launch the app again](#markdown-header-launch-the-app-again)

<!-- /TOC -->

## Terms

**HOST** means your laptop and **CONTAINER** means a docker container.

## New Concepts

- Docker volumes (bind mounts) so files on your laptop are shared with the container.
- Docker container names
- Ubuntu
- Django
- Postgres
- Docker intercontainer networking

### Docker volumes

Docker has a concept of volumes which allow your laptop (host) to share a filesystem path
with the container.

We're using the -v flag which is by default a _bind_ mount. A _bind_ mount is one in which changes
to the files in the container show up back on the host and changes on the host show up in the
container.

The format of the volume flag is:

`-v /path/on/host:/path/on/container`

We will use _TWO_ different mounts for running two different containers...

### Docker container names

https://docs.docker.com/engine/reference/run/#container-identification

We will be naming our containers when we run them. This will let us easily reference them.

### Ubuntu

The base dockerfile is included. This file sets up a basic ubuntu container ready for us to work from.

`docker pull ubuntu:16.04`

### Postgres

We will be using the Postgres database.

https://www.postgresql.org/

`docker pull postgres`

### Postico

Download and install Postico so we can administer our database.

https://eggerapps.at/postico/

## Instructions


### Build the base image

Make a new directory on your laptop and copy in the Dockerfile and then build it with the tag `class-12`

```
mkdir somepath/to/your/project
cd somepath/to/your/project
docker build -t class-12 .
```

### Copy in the requirements & install in a virtualenv

```
docker run -v $PWD:/opt/project -it class-12 python3 -m venv env
```

#### Breakdown

This command calls docker run (to execute a command in a container)

```
docker run
```

and mounts the current directory where we are at on our laptop (`$PWD`) to the project
directory from the Dockerfile

```
-v $PWD:/opt/project
```

and then it says to run an interactive (-i) terminal (-t) (combined to `-it`) from the
imaged tagged `class-12` (which is expanded to `class-12:latest` for the full tag)

```
-it class-12
```

and execute the command to create a python virtual environment named `env` using the
`venv` module in python3.

```
python3 -m venv env
```

If it ran correctly you should be able to execute `ls` on your laptop and see the env directory.

The resulting container is stopped and is saved under the name `class-12-venv`.

You can see all your stopped containers with `docker ps -a` and you can look specifically for
this container with `docker ps -a | grep class-12`

#### Recap

You ran a specific command in a container to establish a virtual env for your project.

### Create & install requirements.txt

Create a file called `requirements.txt` with the following items on your laptop:

```
django==2.0
```

Now install with a container starting from our image with your

```
docker run -v $PWD:/opt/project -it class-12 ./env/bin/pip3 install -r requirements.txt
```

And to confirm that with worked you can see on your laptop that django has been installed:

```
ls env/lib/python3.5/site-packages
```

### Create a sample django project

Now we will create a sample django project:


```
docker run -v $PWD:/opt/project -it class-12 ./env/bin/django-admin startproject mysite
```

And you should now see "mysite" when you run `ls` on your laptop:

```
$ ls -l1
Dockerfile
README.md
env
mysite
requirements.txt
```

### Run the sample server

```
docker run -v $PWD:/opt/project -p 8000:8000 -it class-12 ./env/bin/python3 mysite/manage.py runserver 0.0.0.0:8000
```

Now navigate to `http://127.0.0.1:8000/` in a browser!

Shutdown with ctrl+c when you're finished.

## Postgres


### Switch to postgres

Update `mysite/mysite/settings.py` and replace the database config with the following:

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'project-db',
        'USER': 'unc',
        'PASSWORD': 'tarheels',
        'HOST': 'postgres',
        'PORT': '5432',
    }
}
```

and run the server again:

```
docker run -v $PWD:/opt/project -p 8000:8000 -it class-12 ./env/bin/python3 mysite/manage.py runserver 0.0.0.0:8000
```

This time we have an error:

```
django.core.exceptions.ImproperlyConfigured: Error loading psycopg2 module: No module named 'psycopg2'
```

Hit ctrl+c again to exit.

So we add `psycopg2` to our `requirements.txt` and run the previous comment to install our requirements.

And run the server again...

Another error!

```
django.db.utils.OperationalError: could not translate host name "postgres" to address: Name or service not known
```

So it tried to connect to the database but there wasn't one running...

Hit ctrl+c and we'll set up the database.

### Run postgres

We will want to save our data from our database. In order to keep our repo size small we will save our
database **outside** our project directory. We will use our home directory but you are welcome to change it.

Just remember if you use a different location to use it for all commands for the database container.

We will use `$HOME/pg-data-583` so on your laptop run this command:

```
mkdir $HOME/pg-data-583
```

And launch the postgres container mounting that location in the container for the location for Postgres's
data files. We look at the Docker Hub page for the Postgres image https://hub.docker.com/_/postgres/
to see that it recommends using a subdirectory to contain the data when using an fs mountpoint (which we are
with the `-v` flag).

```
docker run -v $HOME/pg-data-583:/var/lib/postgresql/data/pg-data-583 \
--env PGDATA=/var/lib/postgresql/data/pg-data-583 \
--name class-12-pg \
-p 5432:5432 \
-d postgres
```

### Launch Postico

Launch Postico and create a new connection to `localhost` on port `5432`.

Use the username `postgres` and the password `postgres`.

Create a new database called `project-db`

```
create user unc with password 'tarheels';
grant all on database "project-db" to unc;
```

### Launch the app again

```
docker run -v $PWD:/opt/project -p 8000:8000 --link class-12-pg:postgres -it class-12 ./env/bin/python3 mysite/manage.py runserver 0.0.0.0:8000
```

There is a warning now:

```
You have 14 unapplied migration(s). Your project may not work properly until you apply the migrations for app(s): admin, auth, contenttypes, sessions.
Run 'python manage.py migrate' to apply them.
```

So let's ctrl+c and run that command instead:

```
docker run -v $PWD:/opt/project -p 8000:8000 --link class-12-pg:postgres -it class-12 ./env/bin/python3 mysite/manage.py migrate
```

You should see:

```
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, sessions
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying admin.0001_initial... OK
  Applying admin.0002_logentry_remove_auto_add... OK
  Applying contenttypes.0002_remove_content_type_name... OK
  Applying auth.0002_alter_permission_name_max_length... OK
  Applying auth.0003_alter_user_email_max_length... OK
  Applying auth.0004_alter_user_username_opts... OK
  Applying auth.0005_alter_user_last_login_null... OK
  Applying auth.0006_require_contenttypes_0002... OK
  Applying auth.0007_alter_validators_add_error_messages... OK
  Applying auth.0008_alter_user_username_max_length... OK
  Applying auth.0009_alter_user_last_name_max_length... OK
  Applying sessions.0001_initial... OK
```

Now run our server

```
docker run -v $PWD:/opt/project -p 8000:8000 --link class-12-pg:postgres -it class-12 ./env/bin/python3 mysite/manage.py runserver 0.0.0.0:8000
```

Things are working but I hate this long command. Lets shorten with an alias.

```
alias run_d="docker run -v $PWD:/opt/project -p 8000:8000 --link class-12-pg:postgres -it class-12 ./env/bin/python3"
```

Note using the ```/env/bin/python3 ``` tells it which python to use (the one we just installed)
Now you can run any command using
```
run_d mysite/manage.py
```
