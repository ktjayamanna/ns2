FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive

# Add xenial sources for gcc-4.8
RUN echo "deb http://dk.archive.ubuntu.com/ubuntu/ xenial main" >> /etc/apt/sources.list \
    && echo "deb http://dk.archive.ubuntu.com/ubuntu/ xenial universe" >> /etc/apt/sources.list

RUN apt-get update && apt-get install -y \
    build-essential \
    tcl8.6 \
    tcl8.6-dev \
    tk8.6 \
    tk8.6-dev \
    perl \
    wget \
    tar \
    tree \
    git \
    nano \
    gcc-4.8 \
    g++-4.8 \
    libx11-dev \
    xorg-dev \
    libxmu-dev \
    libperl4-corelibs-perl \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /tmp

# Download and extract NS-2
RUN wget https://sourceforge.net/projects/nsnam/files/allinone/ns-allinone-2.35/ns-allinone-2.35.tar.gz \
    && tar xzf ns-allinone-2.35.tar.gz

# Fix Makefile.in files to use gcc-4.8 and g++-4.8
RUN sed -i 's/@CC@/gcc-4.8/g' /tmp/ns-allinone-2.35/ns-2.35/Makefile.in \
    && sed -i 's/@CXX@/g++-4.8/g' /tmp/ns-allinone-2.35/ns-2.35/Makefile.in \
    && sed -i 's/@CC@/gcc-4.8/g' /tmp/ns-allinone-2.35/nam-1.15/Makefile.in \
    && sed -i 's/@CXX@/g++-4.8/g' /tmp/ns-allinone-2.35/nam-1.15/Makefile.in \
    && sed -i 's/@CC@/gcc-4.8/g' /tmp/ns-allinone-2.35/xgraph-12.2/Makefile.in

# Fix linkstate ls.h error (add 'this->' to erase at line 137)
RUN sed -i '137s/erase(/this->erase(/' /tmp/ns-allinone-2.35/ns-2.35/linkstate/ls.h

# Install NS-2
RUN cd ns-allinone-2.35 && ./install

# Install Python dependencies
RUN pip3 install -r /code/requirements.txt

# Set up environment
ENV PATH="/tmp/ns-allinone-2.35/bin:/tmp/ns-allinone-2.35/tcl8.5.10/unix:/tmp/ns-allinone-2.35/tk8.5.10/unix:$PATH"
ENV LD_LIBRARY_PATH="/tmp/ns-allinone-2.35/otcl-1.14:/tmp/ns-allinone-2.35/lib:$LD_LIBRARY_PATH"
ENV TCL_LIBRARY="/tmp/ns-allinone-2.35/tcl8.5.10/library"

WORKDIR /code
