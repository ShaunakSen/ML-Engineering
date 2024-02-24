## Docker with python

> https://www.youtube.com/watch?v=bi0cKgmRuiA
> https://github.com/python-engineer/python-fun/blob/master/moviepicker/main.py

Check if docker installed

```
PS C:\Users\shaun\OneDrive\Documents\Projects\script-docker> docker -v  
Docker version 20.10.17, build 100c701
```

1. Copy code to `main.py`
2. Create a Dockerfile


We have 3 things

1. Dockerfile
2. Image
3. Container


Dockerfile - blueprint for building images
Image - a template for running containers
Container - actual running process where we have our packaged project

### Define Dockerfile

--- see Dockerfile

### Create docker image

`docker build -t (for tech) [image_name] [location]`

Here we run:

`docker build -t python-imdb .`

In the logs we can see:

`[1/3] FROM docker.io/library/python:3.8@sha256:7d870123fe736cc912528a4f29c380d19f5efa29fc2de6b9d200cfbf92337df5`

This is pulling the python image

`[2/3] ADD main.py . `

Adds entry point

`[3/3] RUN pip install requests beautifulsoup4`

Installs modules

### Start container

```
PS C:\Users\shaun\OneDrive\Documents\Projects\script-docker> docker run python-imdb       
hello
The Lion King (1994), Rating: 8.5, Starring: Roger Allers (dir.), Matthew Broderick, Jeremy Irons
PS C:\Users\shaun\OneDrive\Documents\Projects\script-docker> 
```

Anytime u make changes to the code you will have to rebuild the image

### User input

Uncomment part of code where we take in user input

Rebuild image

```
PS C:\Users\shaun\OneDrive\Documents\Projects\script-docker> docker run python-imdb       
hello
Ikiru (1952), Rating: 8.2, Starring: Akira Kurosawa (dir.), Takashi Shimura, Nobuo Kaneko
Do you want another movie (y/[n])? Traceback (most recent call last):
  File "./main.py", line 45, in <module>
    main()
  File "./main.py", line 39, in main
    user_input = input('Do you want another movie (y/[n])? ')
EOFError: EOF when reading a line
PS C:\Users\shaun\OneDrive\Documents\Projects\script-docker> 
```

It crashes, when we need user args we have to provide addnl args while running

```
PS C:\Users\shaun\OneDrive\Documents\Projects\script-docker> docker run -t -i python-imdb
hello
Room (2015), Rating: 8.1, Starring: Lenny Abrahamson (dir.), Brie Larson, Jacob Tremblay
Do you want another movie (y/[n])? y
Inception (2010), Rating: 8.7, Starring: Christopher Nolan (dir.), Leonardo DiCaprio, Joseph Gordon-Levitt
Do you want another movie (y/[n])? y
Full Metal Jacket (1987), Rating: 8.2, Starring: Stanley Kubrick (dir.), Matthew Modine, R. Lee Ermey
Do you want another movie (y/[n])? n
PS C:\Users\shaun\OneDrive\Documents\Projects\script-docker> 
```

-t : pseudo terminal
-i: interactive


## Fast api example

See /fast_api_example

Dockerfile:

```
FROM python:3.10.10

# set working directory
WORKDIR /fastapi-app 

# copy requirements.txt into working dir
COPY requirements.txt .

RUN pip install -r requirements.txt

COPY ./app ./app

CMD [ "python", "./app/main.py"]
```

Build:

`docker build -t python-fastapi .`

Run:

`docker run -p 8000:8000 python-fastapi`

In docker desktop:

![](https://gcdnb.pbrd.co/images/I6Zorit94Fs5.png)

We can see this container running

To go into the shell, we can click the "open in terminal" button next to the image

Or we can do this from our own terminal

```
(shaunak_personal) ➜  ~ docker ps
CONTAINER ID   IMAGE            COMMAND                  CREATED         STATUS         PORTS                    NAMES
7ba8908dcd2b   python-fastapi   "python ./app/main.py"   3 minutes ago   Up 3 minutes   0.0.0.0:8000->8000/tcp   stupefied_galois
(shaunak_personal) ➜  ~ 
```

We can copy this container id


```
(shaunak_personal) ➜  ~ docker exec -it 7ba8908dcd2b /bin/sh                                                    
# ls
app  requirements.txt
# 
```

Now we are in the docker shell for that container
