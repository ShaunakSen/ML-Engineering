# Kubernetes Introduction

<aside>
👉🏻 [https://www.youtube.com/watch?v=VnvRFRk_51k](https://www.youtube.com/watch?v=VnvRFRk_51k)

</aside>

Kubernetes is an open source cloud orchestration tool

- it manages containers like Docker containers/other containers
- Basically helps us manage apps made up of 100s of containers and helps us manage them in diff envs like physical machines, VMs or cloud envs or hybrid envs

## The need

The rise of microservices caused inc in usage of container tech as containers offered the perfect host for small independent apps

We need a way to manage these containers across diff envs

## Features

- High availability or no downtime - always accessible
- Scalability or high performance
- Disaster recovery - backup and restore - say if servers break down, the infra has backup and restore features

## Basic Architecture

![https://i.imgur.com/tmPobqg.png](https://i.imgur.com/tmPobqg.png)

We have a main master node and a bunch of worker nodes connected to it

Each node has a Kubelet process running on it 

- Kubelet is a kubernetes process that makes it possible for the cluster nodes to communicate and execute tasks

Each worker node has docker containers of diff apps deployed on it

- depending on workload distribution there are diff no of docker containers running on the worker nodes
- The worker nodes are the places where the actual applications are running

What runs on master node? Master node runs several Kubernetes processes that are necessary to run and manage the cluster

![https://i.imgur.com/zCJNMfz.png](https://i.imgur.com/zCJNMfz.png)

- one of these is an API server, which also is a container
- This acts as an entry point to the kubernets cluster
- This is the process which the different kubernetes clients will talk to
    - So if u have the kubernetes UI for dashboard or an API if u are using some scripts or cmd tool - all talk to API server
- Another process is the control manager - this keeps an overview of whats happening in the cluster - repair needed - if some container died and needs to be restarted
- another app is scheduler - schedules containers on diff nodes based on workload and available server resources on each node - basically an intelligent process that decides **on which worker node the next container process is to be scheduled on based on available resources and required load**
- Another component is etcd key value storage - holds at any time the current state of kub cluster - has all config, status data of each node and each container
    - backup and restore is done using these etcd snapshots

![https://i.imgur.com/x73rhS0.png](https://i.imgur.com/x73rhS0.png)

Lastly bw the master and worker nodes, lies a virtual nw which enables the master nodes and worker nodes to talk to each other - this spans all nodes that are part of the cluster - turns all nodes inside the cluster into one powerful machine that has the sum of all resources of indv nodes

- worker nodes actually are the nodes running the apps (containers) so are much bigger and have more resources
- master only runs these master processes so does not need so many resources
- but master node is much more imp  - if we lose master access, we cant access cluster - so we need backup of master
- At least 2 or more masters are needed

## Basic concepts

![https://i.imgur.com/3tF6BqK.png](https://i.imgur.com/3tF6BqK.png)

**Container-** smallest unit that a kub user configures and interacts with

**Pod** - Each pod is a wrapper of one or more containers

On each worker node we have multiple pods, inside each pod we have one or more containers

- **usually per application we have one pod**
    - so when we might have multiple containers within a pod is when we have a main app that needs some helper containers
    - so a db app might be its own pod and so will a message broker, server, java app etc

The virtual nw that spans the kubernetes cluster - it assigns each pod its own IP address

- so each pod acts like its own self contained server
- they communicate with each other using their own internal ip addresses

NOTE: In kubernetes we do not configure or create containers, we work with pods, which is an abstraction layer over containers

Pod is a component of kub which manages containers running within itself - so when container stops/dies, it will be automatically restarted

- Pods can also die, but when it dies a new pod is created and gets a new IP addr - this can be v inconvenient for other pods that communicate with this pod
- So we need another component called a **service which acts like a substitute to those IP addresses**
- So instead of communication via IP addresses the communication happens via services

![https://i.imgur.com/SeZwKCr.png](https://i.imgur.com/SeZwKCr.png)

- When pod dies, and gets recreated, service stays in place and does not change
- Service has 2 roles
    - serve permanent IP addresses for pod-pod communication
    - acts as load balancers

## Example config

All config in a kub cluster actually goes through the master node’s API server process

- kub clients like UI, API, CLI etc. talk to API server and send their config request to the API server which is the **entry point to this cluster**
- request can be in YAML or JSON

![https://i.imgur.com/G884IR8.png](https://i.imgur.com/G884IR8.png)

Lets have a look at an example request:

![https://i.imgur.com/FtyJM7W.png](https://i.imgur.com/FtyJM7W.png)

```yaml
kind: Deployment
- we (the client app) is sending a req to kub to configure a component called Deployment
Deployment is a template for creating pods
replicas: 2
- we want to create 2 replica pods called my-app
containers: name, image, env
- we want to create 2 replica pods called my-app with each pod having a container based on my-image running inside
- we also configure the env vars and port configuartions of this container inside the pod
```

As we see the config req is **declarative -**  we declare our desired outcome and kub tries to meet that

ex : we declare that we want 2 pod replicas, if one dies the controller manager will see that the “is” and “should” states are diff so `desired state != actual state` so it will try to recover or restart the 2nd replica