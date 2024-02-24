FROM python:3.10.10

# set working directory
WORKDIR /fastapi-app 

# copy requirements.txt into working dir
COPY requirements.txt .

RUN pip install -r requirements.txt

COPY ./app ./app

CMD [ "python", "./app/main.py"]

