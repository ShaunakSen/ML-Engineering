# we can use comments here
# specify a base image
# will pull this image from dockerhub 

## ADD [file] [dest] - here we are adding main.py in the current directory of our container
FROM python:3.8

ADD main.py .

## next we need to install dependencies

RUN pip install requests beautifulsoup4

## entry command when we start container

CMD ["python", "./main.py"]
