# pull official base image
FROM python:3.6

# set work directory
WORKDIR /usr/src/websocket

# set environment variables

# install mysql dependencies

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy entrypoint.sh
COPY ./entrypoint.sh .

# copy project
COPY . .

CMD ["/usr/src/websocket/entrypoint.sh"]
