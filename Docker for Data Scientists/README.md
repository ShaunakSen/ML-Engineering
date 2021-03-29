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

Now devs can simply build the app, and the dev and dev ops team works together to create the docker file, which is then used to create an image of the app. The image can now run on any host with docker installed and the image can be now used to deploy the application by the dev ops team.