## Docker End to End

> https://www.youtube.com/playlist?list=PLZoTAELRMXVNKtpy0U_Mx9N26w8n0hIbs

---


### Docker Basics

We need a base image

Lets say base image is python 3.11

On top we use flask, pandas etc.

Now we dockerize all of this and we can share

#### FROM command

`FROM base_image` -> this is the base image we want

#### COPY command 

Used to copy folders from my local system to docker system

#### EXPOSE command

used to expose some ports, so that we can access the app through the port

#### WORKDIR

working directory of code inside docker image

#### RUN

run any commands - `pip install -r reqirements.txt`

#### CMD

run the starting point of the application - `python app.py`


### 1. Write the Dockerfile

```
FROM bitnami/python:3.12.5
COPY . /usr/app/
EXPOSE 5000
WORKDIR /usr/app/
RUN pip install -r requirements.txt
CMD python app.py
```

### 2. Build the Docker image

`(docker-project-py3.12) (base) ➜  docker-end-to-end git:(master) ✗ docker build -t simple_api .`

The command `docker build -t simple_api .` is used to create a Docker image from a Dockerfile. Here's a breakdown of what each part of the command does:

1. **`docker build`**: This is the Docker command used to build an image from a Dockerfile.

2. **`-t simple_api`**: The `-t` flag allows you to tag the image with a name (`simple_api` in this case). This makes it easier to reference the image later when you want to run a container from it. The tag `simple_api` acts as a shorthand name for the image.

3. **`.`**: This specifies the build context for Docker, which is the current directory (`.`). Docker will look for a Dockerfile in this directory to use as the instructions for building the image.

In summary, this command will look for a Dockerfile in the current directory and use it to build a Docker image named `simple_api`.

### 3. Run the Docker image

```
(docker-project-py3.12) (base) ➜  docker-end-to-end git:(master) ✗ docker run -p 5000:5000 simple_api 
 * Serving Flask app 'app'
 * Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5000
 * Running on http://172.17.0.2:5000
Press CTRL+C to quit
```

Check which docker images are running: `docker ps`


The command `docker run -p 5000:5000 simple_api` is used to start a Docker container from an image called `simple_api` and map a port from the container to the host machine. Let's break down each part of this command:

1. **`docker run`**: This command is used to create and start a new Docker container from a specified Docker image.

2. **`-p 5000:5000`**: The `-p` flag is used to publish a container's port(s) to the host. The syntax `host_port:container_port` specifies that port `5000` on the host machine is mapped to port `5000` on the Docker container.
   
   - **`5000:5000`**: 
     - The **first `5000`** is the port on your local host machine (your computer).
     - The **second `5000`** is the port inside the Docker container where the application inside the container is running.

3. **`simple_api`**: This is the name (or tag) of the Docker image from which you want to create a container. In this case, the image is named `simple_api`.

### What This Command Does

- **Starts a new container** from the `simple_api` image.
- **Maps port 5000** of the host machine to **port 5000** of the container. This means that any network traffic sent to port `5000` on the host machine will be forwarded to port `5000` in the container.
- The application running inside the Docker container will listen on port `5000` (as defined in the image setup), and you will be able to access this application on your local machine by going to `http://localhost:5000`.

### Example Scenario

If `simple_api` is an API service built to listen on port `5000`, running the above command would:
- Start the API service inside a Docker container.
- Allow you to access this API service from your host machine using `http://localhost:5000`.

### Key Points

- **Port Mapping (`-p`)**: The `-p` flag is crucial when you want to expose an internal port of a Docker container to the outside world. It allows your local machine to interact with services running inside the Docker container as if they were running directly on your machine.
- **Accessing the Service**: After running this command, you can access the API or application running inside the container by navigating to `http://localhost:5000` in a web browser or any tool like `curl` or Postman.
