# pull official base image
FROM python:3.8
# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt
RUN pip install requests-html


# copy project
COPY . .

CMD ["python3", "worker.py"]