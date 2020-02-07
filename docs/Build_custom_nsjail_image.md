# Build custom nsjail image

When you clone [https://github.com/google/nsjail/](https://github.com/google/nsjail/blob/master/Dockerfile). There is Dockerfile that used to build nsjail docker image.

    //https://github.com/google/nsjail/blob/master/Dockerfile
    FROM ubuntu:16.04
    
    RUN apt-get -y update && apt-get install -y \
        autoconf \
        bison \
        flex \
        gcc \
        g++ \
        git \
        libprotobuf-dev \
        libnl-route-3-dev \
        libtool \
        make \
        pkg-config \
        protobuf-compiler \
        && rm -rf /var/lib/apt/lists/*
    
    COPY . /nsjail
    
    RUN cd /nsjail && make && mv /nsjail/nsjail /bin && rm -rf -- /nsjail

To build for ubuntu18.04, just change the value of `FROM` to ubuntu:18.04.

    //nsjail:18.04
    FROM ubuntu:18.04 // <== Just change this
    
    RUN apt-get -y update && apt-get install -y \
        autoconf \
        bison \
        flex \
        gcc \
        g++ \
        git \
        libprotobuf-dev \
        libnl-route-3-dev \
        libtool \
        make \
        pkg-config \
        protobuf-compiler \
        && rm -rf /var/lib/apt/lists/*
    
    COPY . /nsjail
    
    RUN cd /nsjail && make && mv /nsjail/nsjail /bin && rm -rf -- /nsjail