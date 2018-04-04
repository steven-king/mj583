## Deploying to production with Docker images and containers
Here is a video by @leetrout that walks through all of this:
https://www.youtube.com/watch?v=Dz9jVx0kTbc&feature=youtu.be


1. Edit docker file to include all local files needed.

open the Dockerfile and add this to the bottom.

```
# Adding all local code files
COPY . .

```

This says copy everything in the current directory (all our code) to the current, in this case the top directory of the image.
This lets us not use the -v flag.
NOTE: All future code changes will require you to rebuild from this point on.

2. Build the image
```
docker build -t nobel-app-prod .
```

3. Run the container with a new version of the command
```
docker run -p 8000:8000 -d nobel-app-prod ./env/bin/python3 nobel/manage.py runserver 0.0.0.0:8000

```
Note I have removed the volumn and the interactive terminal

4. What if you made some changes.
Watch me change a css file and a template file (one is static, the template is not.)

```
docker ps
docker kill [id]
```
```
This command adds in the local volumn for testing.
docker run -v $PWD:/opt/project -d -p 8000:8000 nobel-app-prod ./env/bin/pip3 install -r requirements.txt
```

Let's reset:
```
docker ps
docker kill [id]

```

When you are ready to deploy changes you will always have to:
A. Collect Static
```
docker run -v $PWD:/opt/project -it -p 8000:8000 nobel-app ./env/bin/python3 nobel/manage.py collectstatic
```

Test locally
```
docker run -v $PWD:/opt/project -it -p 8000:8000 nobel-app-prod ./env/bin/python3 nobel/manage.py runserver 0.0.0.0:8000
```
B. Run Docker build to copy to new files into the image.
```
docker build -t nobel-app-prod:180403-01 .
```

5. Now we need to zip up this image so we can move it to a server.
A.
``` docker images
```
B. Copy the image name and run,
```
docker save nobel-app-prod:180403-01 | gzip > deployment.tar.gz
```

6. Good practice, edit .gitignore to include nobel/static and the gzip files
```
.pyc
nobel/static
deployment.tar.gz

```

7. For Digital Ocean we need an SSH Key.

NOTE: DO NOT use default file. It might mess up other stuff
```
ssh-keygen
```

Instead of the default, copy the path (Users/username/.ssh)
Then add the name of the key. I would call this key mj583 so the new path is for example
Users/stking/.ssh/mj583

Leave passphrase empty

```
ssh-add your/path/mj583

```

To view the Public key use cat
```
cat your/path/mj583.pub
```

8. Signup for digital Ocean
Sign up, confirm email, and add card.

9. Create a new droplet
Choose Smallest/Cheapest
New York 1
Add your SSH key by copy and paste the entire multi-line string from the terminal
Change the name to something that makes sense like nobbel-app-prod (my docker image name)
Create and it takes a few minutes.

10. SSH to connect to your new server/droplet
```
ssh root@yourIPAddress

```
Yes, you are sure.

Check to see if Docker is actually running (no error, just a blank/empty list)

```
docker ps
```
Type exit to end

11. Copy the deployment to the server using secure copy which uses SSH
```
scp deployment.tar.gz root@YourIPAddress:deployment.tar.gz
```

12. SSH to manage the server.
```
ssh root@yourIPAddress

```

```
gunzip deployment.tar.gz

```
then run
```
docker load -i deployment.tar
```
then to start the server:
```
docker run -p 80:8000 -d nobel-app-prod:180403-01 ./env/bin/python3 nobel/manage.py runserver 0.0.0.0:8000
```

Test it by viewing your IP address.
