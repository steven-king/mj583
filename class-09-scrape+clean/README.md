To create your own Docker Image with new requirements

``` docker buid -t tagname . ```

Note the . is important. It is the local path of the dockerfile


To run your docker image

``` docker run -p 9000:9000 -d -t tagname ```

You can add files to your docker image on the docker file using

``` COPY filename /path/to/dir/with/dockerfile/ ```

ex. ``` COPY "filename.ipynb" . ```

Note the . is the local path.

