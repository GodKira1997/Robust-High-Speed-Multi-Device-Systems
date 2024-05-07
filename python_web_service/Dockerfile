FROM amazonlinux:latest

#
RUN yum update
RUN yum install -y python3
RUN yum install -y python3-pip
RUN yum install -y wget

# Install Miniconda
RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda.sh \
    && bash miniconda.sh -b -p /opt/conda \
    && rm miniconda.sh

# Expose port 25565
EXPOSE 8080

RUN mkdir -p /opt/home
RUN mkdir -p /opt/home/static
WORKDIR /opt/home

ADD requirements.txt /opt/home

# Set environment variables
ENV PATH="/opt/conda/bin:${PATH}"

RUN conda update -n base -c defaults conda && conda install -c conda-forge -y liblsl
RUN conda install -c conda-forge paho-mqtt

RUN ["pip", "install", "-r", "/opt/home/requirements.txt"]

ADD server.py /opt/home
ADD app.html /opt/home
ADD heartbeat_response.py /opt/home
ADD lsl_receiver.py /opt/home
ADD static /opt/home/static

# Start the server
ENTRYPOINT ["python3", "server.py"]