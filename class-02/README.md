# Starting from scratch

1. `docker build -t class-02-exercise-01 .`
2. `docker run -p 9000:9000 -d -t class-02-exercise-01`
3. Open http://127.0.0.1:9000
4. Click on the nobel winners notebook
5. Cell > Run All
6. Follow along from Chapter 3. Sorting the keys will not work as-is...
7. Save your work using the save icon
8. Download your notebook File > Download as > Notebook (.ipynb)
9. Commit & push your Docker container as a new image (see below)

## Committing a new image

Run `docker ps` to find the container ID

```
➜  class-02 git:(class-02) docker ps
CONTAINER ID        IMAGE                  COMMAND                  CREATED             STATUS              PORTS                    NAMES
8478971ee193        class-02-exercise-01   "/bin/sh -c '/usr/..."   17 minutes ago      Up 16 minutes       0.0.0.0:9000->9000/tcp   zealous_kare
```

Use the value from the container ID along with your Docker cloud username to
create a new tag named `class-02-exercise-01` within YOUR repo

Run `docker commit <CONTAINER ID> <REPO NAME>:<TAG NAME>`

So if my Docker cloud username was sallyjones and my repository was data-viz my
command would look like:

`docker commit 8478971ee193 sallyjones/data-viz:class-02-exercise-01`

## Pushing a new image

You can push a new image to Docker cloud using the repository name. Assuming
the values from the example above I could run:

`docker push sallyjones/data-viz:class-02-exercise-01`

And view my results at https://cloud.docker.com/swarm/leetrout/repository/docker/leetrout/unc-data-viz/general

# Wrapping up

When finished **BE SURE** you have downloaded your notebook and committed your
docker image! Your work will be destroyed by the following command!

Clean up your docker instances by killing the running instance. Run `docker ps`
and again using the container ID:

`docker kill <CONTAINER ID>`
