# Basics of Docker

Credits: https://www.youtube.com/watch?v=fqMOX6JJhGo

## Motivation and Overview

Imagine we have a tech stack as:

1. Tensorflow
2. scikit-learn
3. xgboost
4. streamlit for building apps
5. ... and so on

Now streamlit may require a version of numpy which is not supported by our current version of xgboost. This causes a lot of dependency conflicts. Also we might need to update our frameworks and every time this happens we need to check for compatibility issues.  New devs need to be trained and their systems need to be setup which is a complex process. Also this does not scale across diff os

With docker each tech gets its own dependecies and libraries, all on the same VM/OS but within separate containers/environments

We build the docker config once and all devs can get started with a simple docker run command irrespective of OS they are on

## Containers

Containers are isolated envs, they have their own processes, services, nw interfaces, and mounts, just like VMs, but they share the same OS kernels

Containers are an older tech, docker uses containers, more specifically LXC containers

Setting up containers is hard as they are very low level and that is where docker comes in

![https://i.imgur.com/phL9j18.png](https://i.imgur.com/phL9j18.png)

All OS (say ubuntu fedora, opeSUSE) consists of:

1. OS Kernel: interacts with underlying hardware; here all OS kernels are same (linux) but differs in software
2. Software: diff UI/drivers/file managers etc

The common linux kernel exists across all OS

We said that docker containers share the underlying kernel; what does that mean?

Say we have Ubuntu OS with docker installed on it

Docker can run any flavor of OS on top of it as long as they are based on same kernel; here in this case Linux

If underlying OS is Ubuntu, docker can run a container based on Debian/Fedora/SUSE etc. Each container has the underlying sw that makes these OS diff and docker uses the underlying kernel of the docker host

We cant run a windows based container on a docker host with Linux on it, for that we will require Docker on a windows server

![https://i.imgur.com/uDVW89H.png](https://i.imgur.com/uDVW89H.png)

But we can install docker on windows and run a container based on Linux - what happens here?

- Windows runs the Linux container on a Linux VM under the hoods
- Its a Linux container on a Linux VM on Windows

![https://i.imgur.com/WKPj1MH.png](https://i.imgur.com/WKPj1MH.png)

Often its not a question of container or VM as they are diff things totally. When we have large environments with multiple app containers running on multiple docker hosts we  might run the container on virtual docker hosts

![https://i.imgur.com/GBQNZea.png](https://i.imgur.com/GBQNZea.png)

### DockerHub

We already have lot sof containerized applications available on DockerHub which is a public repo

We can simply download a docker image from this repo and run it using docker run command

docker run nodejs : runs an instance of nodejs on the docker host

### Image vs container

Image is like a template used to create one or more containers. Containers are running instances of images that are 

isolated and have their own environments and set of processes

![https://i.imgur.com/RWH4Ruy.png](https://i.imgur.com/RWH4Ruy.png)

### Docker in the devops culture

Now devs can simply build the app, and the dev and dev ops team works together to create the docker file, which is then used to create an image of the app. The image can now run on any host with docker installed and the image can be now used to deploy the application by the dev ops team.

## Docker on Windows

We learned that containers share the underlying OS kernel and as a result we cannot have a windows container running on Linux host or vice-versa we need to keep this in mind. We have a few options

1. Docker on windows using Docker Toolbox
2. Docker Desktop for Windows

### Docker Toolbox

You can use a virtualbox and setup a Linux VM and then run docker on it. You are working within the VM. Docker toolbox comes with the set of sw that makes this process easier

### Docker Desktop

This uses the native virtualization technology for windows - Microsoft Hyper-V.

This option is only supported for Windows 10 enterprise or professional Edition and on Windows Server 2016 because both these operating systems come with hyper-v support by default now

### Setting up

- Installed docker desktop
    - Installed docker for us
- check its working

    ```bash
    docker version
    ```

- pull a container from dockerhub: [https://hub.docker.com/r/docker/whalesay](https://hub.docker.com/r/docker/whalesay)
- Run this container

    ```bash
    docker run docker/whalesay cowsay mini
    ```

## Docker commands

**`docker run`**: run a container from an image

`docker run nginx` : will run an instance of the nginx app on the docker host if image exists, else will go to docker hub and pull it

**`docker ps`**: lists all running containers, container id, status, name of image used to run the container etc.

Each container gets a random id and name created. Run with -a flag to get list of all running + previously run containers

```bash
PS C:\Users\shaun> docker ps -a
CONTAINER ID   IMAGE                    COMMAND                  CREATED          STATUS                      PORTS     NAMES
4ac70bf46457   docker/whalesay:latest   "/bin/bash"              4 minutes ago    Exited (0) 4 minutes ago              cranky_elgamal
ec62f7de524e   docker/whalesay          "cowsay mini"            27 minutes ago   Exited (0) 27 minutes ago             cranky_wiles
d19e65e7b272   docker/whalesay          "cowsay boo"             27 minutes ago   Exited (0) 4 minutes ago              elastic_raman
6a415ffae254   alpine/git               "git clone https://g…"   39 minutes ago   Exited (0) 39 minutes ago             repo
```

**`docker stop <container_id/name>`:** stop running containers

**`docker images`**: view a list of images

```bash
PS C:\Users\shaun> docker images
REPOSITORY          TAG       IMAGE ID       CREATED          SIZE
docker101tutorial   latest    5106ace3bc71   39 minutes ago   27.9MB
alpine/git          latest    a939554ad0d0   5 weeks ago      25.1MB
docker/whalesay     latest    6b362a9f73eb   5 years ago      247MB
```

`**docker rmi <image_id>**`: removes an image

Lets try to delete the image for whalesay

```bash
PS C:\Users\shaun> docker rmi 6b362a9f73eb
Error response from daemon: conflict: unable to delete 6b362a9f73eb (must be forced) - image is being used by stopped container 4ac70bf46457
```

We cant delete the image because a container might still use it; we need to delete the container first

**`docker rm <container_id/name>`:** delete the container

```bash
PS C:\Users\shaun> docker rm 4ac70bf46457
4ac70bf46457
### now we can delete the image
PS C:\Users\shaun> docker rmi 6b362a9f73eb
Untagged: docker/whalesay:latest
Untagged: docker/whalesay@sha256:178598e51a26abbc958b8a2e48825c90bc22e641de3d31e18aaf55f3258ba93b
Deleted: sha256:6b362a9f73eb8c33b48c95f4fcce1b6637fc25646728cf7fb0679b2da273c3f4
Deleted: sha256:34dd66b3cb4467517d0c5c7dbe320b84539fbb58bc21702d2f749a5c932b3a38
Deleted: sha256:52f57e48814ed1bb08a651ef7f91f191db3680212a96b7f318bff0904fed2e65
Deleted: sha256:72915b616c0db6345e52a2c536de38e29208d945889eecef01d0fef0ed207ce8
Deleted: sha256:4ee0c1e90444c9b56880381aff6455f149c92c9a29c3774919632ded4f728d6b
Deleted: sha256:86ac1c0970bf5ea1bf482edb0ba83dbc88fefb1ac431d3020f134691d749d9a6
Deleted: sha256:5c4ac45a28f91f851b66af332a452cba25bd74a811f7e3884ed8723570ad6bc8
Deleted: sha256:088f9eb16f16713e449903f7edb4016084de8234d73a45b1882cf29b1f753a5a
Deleted: sha256:799115b9fdd1511e8af8a8a3c8b450d81aa842bbf3c9f88e9126d264b232c598
Deleted: sha256:3549adbf614379d5c33ef0c5c6486a0d3f577ba3341f573be91b4ba1d8c60ce4
Deleted: sha256:1154ba695078d29ea6c4e1adb55c463959cd77509adf09710e2315827d66271a
```

**`docker pull <name> and docker run <name>`:** the run command downloads the image and runs the container. pull simply downloads the image. For example `docker run ubuntu` runs an instance of ubuntu image and exits immediately. Why is that? Unlike VMs containers are not meant to host an OS, its designed to run a specific task, once done, it exits. **The container lives only as long as the process inside it is alive**. If the image is not running any service, as in ubuntu we can ask docker to run a process using the run command, for e.g: `docker run ubuntu sleep 5`. After 5 s the container will stop

**`docker exec <container_name> command`**: execute a command on a running container. if the container is running, we can use exec to run a command, here we are using it to view contents of the hosts file while the container is running (sleep for 100s)

![https://i.imgur.com/2EIzwic.png](https://i.imgur.com/2EIzwic.png)

**attach/detach**: Say there is a simple web app called kodekloud/simple-webapp. When we run `docker run kodekloud/simple-webapp,` it runs in attach mode, i.e, we are attached to the console of the stdout of the container, we cant do anything else until we stop it

`docker run -d kodekloud/simple-webapp`: runs in detach mode, in the background. Attach back using `docker attach <first few chars of container id>`

![https://i.imgur.com/aJFKww0.png](https://i.imgur.com/aJFKww0.png)

Pull the image: nginx:1.14-alpine but dont create  a container: `docker pull nginx:1.14-alpine`

Run the command `docker run --name webapp nginx:1.14-alpine`: This runs a container with the nginx:1.14-alpine image and name it webapp