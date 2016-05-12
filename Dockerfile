# Set the base image to Ubuntu
FROM ubuntu

# File Author / Maintainer
MAINTAINER Paul Scott <pscott209@gmail.com>

# Add the application resources URL
# RUN echo "deb http://archive.ubuntu.com/ubuntu/ $(lsb_release -sc) main universe" >> /etc/apt/sources.list

# Update the sources list
RUN apt-get update

# Install basic applications
RUN apt-get install -y tar git curl nano wget dialog net-tools build-essential

# Install Python and Basic Python Tools
RUN apt-get install -y python python-dev python-distribute python-pip

# Copy the application folder inside the container
RUN git clone https://github.com/paulscott56/AdaptService.git /adapt

RUN pip install -e git+https://github.com/mycroftai/adapt#egg=adapt-parser

# Get pip to download and install requirements:
RUN pip install -r /adapt/requirements.txt

# Expose ports
EXPOSE 5000

# Set the default directory where CMD will execute
WORKDIR /adapt

# Set the default command to execute    
# when creating a new container
CMD python ErrorService.py
