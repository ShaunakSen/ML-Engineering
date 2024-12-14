## Docker Containers and Kubernetes Fundamentals

> Notes on the course by Guy Barrette and FreeCodeCamp

- https://guybarrette.com/
- https://www.youtube.com/watch?v=kTp5xUtcalw

---

### Containers

![](https://imgur.com/x6Q22Fd.png)

__VM vs containers__:

![](https://imgur.com/cBmkddf.png)

- VMs comprise the app + OS into an isolate env. 
- Containers use the host OS kernel, so are much faster to boot
- Since containers have no OS, they use lesser memory


Containers are mad up of layers
- base OS
- customizations
- applications


__Container Resistry__: Place where u deploy your containers - DockerHub, Google Container Registry etc.

#### Orchestrator:

![](https://imgur.com/sZgLDiy.png)


#### Docker:

Basically an Open Source Container Runtime

#### Docker CLI

![](https://imgur.com/u5qWLtO.png)

`imageName`: name of image as we find it in the conatiner registry

`containerName`: name of the running container

![](https://imgur.com/9VjVtcX.png)

![](https://imgur.com/yimUUXG.png)

![](https://imgur.com/NTIFkTp.png)

### Images vs containers in Docker

In Docker, **images** and **containers** are two fundamental concepts, but they serve different purposes. Here's a comparison of the two in the context of Docker:

### Docker Image:
- **Definition**: A Docker image is a **read-only template** that contains the application code, dependencies, libraries, and environment configurations needed to run an application.
- **Purpose**: Images serve as a blueprint for creating containers. They are static and don’t change when containers are running.
- **Layers**: Images are built in layers, where each layer represents a file change or modification. This layered architecture allows for efficient storage and reusability.
- **Creation**: You typically create images using a `Dockerfile`, which defines the steps to set up the environment and application in an image.
- **Examples**: Official images like `nginx`, `mysql`, or custom images built from a `Dockerfile` for your own application.

### Docker Container:
- **Definition**: A Docker container is a **runtime instance** of a Docker image. It's a running environment that is created from an image and can be started, stopped, or deleted.
- **Purpose**: Containers allow you to run applications in isolated environments. Unlike images, containers are **ephemeral** (they can be stopped, modified, and restarted).
- **State**: Containers have a writable layer on top of the image, meaning any changes you make (e.g., editing files, installing new software) are applied only to that container. When the container stops, the changes can be lost unless explicitly saved.
- **Creation**: Containers are created using the `docker run` command, which specifies the image to use along with options such as port mappings, environment variables, and volumes.
- **Examples**: A running instance of `nginx` (created from the `nginx` image), a container running a custom Python app, or a database container running PostgreSQL.

### Key Differences:
| **Aspect**        | **Docker Image**                          | **Docker Container**                      |
|-------------------|-------------------------------------------|-------------------------------------------|
| **Nature**        | Blueprint or template                     | Instance of an image (a running process)  |
| **State**         | Static and immutable                      | Dynamic and modifiable                    |
| **Use**           | To create containers                      | To run applications                       |
| **Storage**       | Stored on disk (shared across containers)  | Ephemeral (exists during runtime)         |
| **Lifecycle**     | Built once, reused many times             | Created, started, stopped, removed        |
| **Modification**  | Cannot be changed once built              | Can be modified, but changes are lost unless committed |

In short, a **Docker image** is like a class in programming (defining structure and behavior), and a **Docker container** is like an object (a running instance of that class).


### Running an Nginx container

`docker run -d -p 8000:80 --name webserver nginx`

```
% docker ps -a
CONTAINER ID   IMAGE     COMMAND                  CREATED         STATUS         PORTS                  NAMES
9ae243ddae9e   nginx     "/docker-entrypoint.…"   9 seconds ago   Up 8 seconds   0.0.0.0:8000->80/tcp   webserver
```

If we go to 0.0.0.0:8080 we can see the server running.

The command `docker container exec -it webserver bash` allows you to interactively access a running Docker container named `webserver`.

Here's a breakdown of what it does:
`docker container exec -it webserver bash`

```
(base) rishabhagarwal@Rishabhs-MacBook-Air ~ % docker container exec -it webserver bash
root@9ae243ddae9e:/# ls
bin  boot  dev	docker-entrypoint.d  docker-entrypoint.sh  etc	home  lib  media  mnt  opt  proc  root	run  sbin  srv	sys  tmp  usr  var
root@9ae243ddae9e:/# 
```
`9ae243ddae9e` is container id and we are the __root__ user

- `docker container exec`: This command executes a new process inside a running container.
- `-it`: This is a combination of two flags:
  - `-i`: Keeps the STDIN (input) open, allowing you to interact with the container.
  - `-t`: Allocates a pseudo-TTY, which simulates a terminal connection for better interactive use.
- `webserver`: This is the name of the running container that you created earlier with the `docker run` command (in this case, the `nginx` container running on port 80 and mapped to port 8000 on the host).
- `bash`: This tells Docker to open a Bash shell inside the `webserver` container.

#### Context from your previous command:
The previous command you ran, `docker run -d -p 8000:80 --name webserver nginx`, started an Nginx web server in detached mode (`-d`), mapped port 80 of the container to port 8000 on your host, and gave the container the name `webserver`.

By running the `docker container exec -it webserver bash` command, you're opening an interactive Bash session inside the running `webserver` container. This allows you to inspect or modify the container's environment, for example, by checking logs, modifying configuration files, or installing additional packages.

This is super useful for debugging/troubleshooting


Remove the container:

```
(base) rishabhagarwal@Rishabhs-MacBook-Air ~ % docker stop webserver
webserver
(base) rishabhagarwal@Rishabhs-MacBook-Air ~ % docker ps -a                            
CONTAINER ID   IMAGE     COMMAND                  CREATED          STATUS                     PORTS     NAMES
9ae243ddae9e   nginx     "/docker-entrypoint.…"   12 minutes ago   Exited (0) 4 seconds ago             webserver
(base) rishabhagarwal@Rishabhs-MacBook-Air ~ % docker rm webserver
webserver
(base) rishabhagarwal@Rishabhs-MacBook-Air ~ % docker ps -a       
CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES
(base) rishabhagarwal@Rishabhs-MacBook-Air ~ % 
```

However the __image__ that was used to build the container is still there on my system

```
(base) rishabhagarwal@Rishabhs-MacBook-Air ~ % docker images
REPOSITORY                                TAG                                        IMAGE ID       CREATED         SIZE
nginx                                     latest                                     6e8672ddd037   6 weeks ago     193MB
```


```
(base) rishabhagarwal@Rishabhs-MacBook-Air ~ % docker rmi nginx
Untagged: nginx:latest
Untagged: nginx@sha256:b5d3f3e104699f0768e5ca8626914c16e52647943c65274d8a9e63072bd015bb
Deleted: sha256:6e8672ddd037e6078cad0c819d331972e2a0c8e2aee506fcb94258c2536e4cf2
Deleted: sha256:85115b3f4a6d5627d8a46ee3f29cd9987a8235614f53cc3ac7873abf92182c93
Deleted: sha256:45ad8e0c31f7363713d04615b0638fb15e30f5fbb4cb72f52a4e9832cca8ba8d
Deleted: sha256:6882c03ff14c04309634a4cd619be01f5db3743900043d9ec328b2328debf5cf
Deleted: sha256:55a2eb9f3aef77461449e0717dc42d304e84b9ef292bab442175491c5ee5e9c8
Deleted: sha256:0cd79773e1182e3a7895bfe0d04db158ad1d4315f5e3ecf77633f43a6484d199
Deleted: sha256:6dd322a34931537c364fded69c43cedd194af70c5c53cf20eae076d9ab692281
Deleted: sha256:054df1200f3e1d70e2ebeafa03c965d0dd34e7dab90b4ea24963352e5590b573
(base) rishabhagarwal@Rishabhs-MacBook-Air ~ % 
```

NOTE: Now i used the "name" of the image not the running container

The multiple delete statements are for all the layers which are deleted

### Building images

![](https://imgur.com/VB04QDq.png)

DockerFile: text file with list of steps required to build an image


#### Static html page

We want to setup a new index.html in a server

First we need to get a server (nginx) image and run it as a container

`docker run --publish 80:80 --name webserver nginx`

Next we need to figure out where the index.html is stored within the container

We need to exec into the container

`docker exec -it 0896b682844a9abc44d86c5f11f5c9730fb8d6c0679ea3752cf996fb2865b0c9 /bin/sh`

```
# ls
bin  boot  dev  docker-entrypoint.d  docker-entrypoint.sh  etc  home  lib  media  mnt  opt  proc  root  run  sbin  srv  sys  tmp  usr  var
# cd usr 
# ls
bin  games  include  lib  libexec  local  sbin  share  src
# cd share
# ls
X11              bug              debianutils  dpkg        gdb       libc-bin     man         nginx        pixmaps   util-linux
base-files       ca-certificates  dict         fontconfig  info      libgcrypt20  maven-repo  pam          polkit-1  xml
base-passwd      common-licenses  doc          fonts       java      lintian      menu        pam-configs  tabset    zoneinfo
bash-completion  debconf          doc-base     gcc         keyrings  locale       misc        perl5        terminfo  zsh
# cd nginx
# ls  
html
# cd html
# ls
50x.html  index.html
# cat index.html
<!DOCTYPE html>
<html>
<head>
<title>Welcome to nginx!</title>
<style>
html { color-scheme: light dark; }
body { width: 35em; margin: 0 auto;
font-family: Tahoma, Verdana, Arial, sans-serif; }
</style>
</head>
<body>
```

NOTE: Doing this through the Docker app is easier as u can exec into the container and open in a terminal directly

We now know where to make the changes

```
# pwd     
/usr/share/nginx/html
```

We now write the Dockerfile

```
FROM nginx:alpine
COPY index.html /usr/share/nginx/html
```

We build the image

`docker build -t webserver-custom:v1 . `

We run the container

`docker run -d -p 8080:80 webserver-custom:v1`


In localhost:8080 we can see the changes made

![](https://imgur.com/5uF0AnR.png)


#### Node site

For our base image we would like to use alpine - which is a lightweight linux distro

As before lets explore running some commands in the container of the image before working on the Dockerfile

`docker pull alpine`

Next we run the container and start an interactive shell in the container

`docker run -it alpine /bin/sh`

Now we are inside the container shell

We run the following commands

```
apk update
apk add nodejs
apk add npm
```

Next we write some simple nodejs code to setup a server

```
const http = require("http");
const hostname = "0.0.0.0";
const port = 3000;

const server = http.createServer((req, res) => {
  res.statusCode = 200;
  res.setHeader("Content-Type", "text/plain");
  res.end("Hello from Node.js inside the container!\n");
});

server.listen(port, hostname, () => {
  console.log(`Server running at http://${hostname}:${port}/`);
});
```

Now we need to write the Docker file

```
FROM alpine:latest
RUN apk update
RUN apk add nodejs
RUN apk add npm
RUN mkdir src
COPY ./ /src
WORKDIR /src
EXPOSE 3000
CMD [ "node", "server.js" ]

```

Build the image:
`docker build -t node-custom:v1 .`

Run the container

`docker run -d -p 3000:3000 node-custom:v1`

### Dockerizing an Express App using vscode 

> See the README in node-app-1







