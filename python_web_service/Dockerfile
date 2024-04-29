FROM amazonlinux:latest

#
RUN yum install -y python3
RUN yum install -y python3-pip

# Expose port 25565
EXPOSE 8080

RUN mkdir -p /opt/home
RUN mkdir -p /opt/home/static
WORKDIR /opt/home




ADD requirements.txt /opt/home
RUN ["pip", "install", "-r", "/opt/home/requirements.txt"]

ADD server.py /opt/home
ADD app.html /opt/home
ADD lsl_reciever.py /opt/home
ADD static /opt/home/static


# Start the server
CMD ["python3", "server.py"]