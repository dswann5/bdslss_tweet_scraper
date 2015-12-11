# Dockerfile to build python and mongodb container image
# Based on ubuntu

FROM ubuntu
RUN apt-get update

# Add the package verification key
RUN apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 7F0CEB10

# Add MongoDB to the repository sources list
RUN echo "deb http://repo.mongodb.org/apt/ubuntu trusty/mongodb-org/3.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.0.list

# Update the repository sources list once more
RUN apt-get update

# Install MongoDB package and python
RUN apt-get install -y python
RUN apt-get install -y python-pip
RUN apt-get install -y git 
RUN apt-get install -y mongodb-org
RUN apt-get install -y build-essential python-dev

# Install pip dependencies from file
RUN pip install tweepy 
RUN pip install pymongo 
RUN pip install nltk 

# Create the default data directory
RUN mkdir -p /data/db

EXPOSE 27017

# Default port to execute the entrypoint (MongoDB)
CMD ["--port 27017"]

# Set default container command
ENTRYPOINT usr/bin/mongod
