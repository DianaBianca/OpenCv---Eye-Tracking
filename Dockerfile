FROM ubuntu

ARG DEBIAN_FRONTEND=noninteractive

WORKDIR /eyetracking

LABEL name="Diana Rodrigues"

RUN apt-get update && apt-get upgrade -y

RUN apt-get install -y software-properties-common

RUN add-apt-repository "deb http://security.ubuntu.com/ubuntu xenial-security main"

RUN apt-get update -y

RUN apt-get install -y build-essential apt-utils

RUN apt-get install -y cmake git libgtk2.0-dev pkg-config libavcodec-dev \
    libavformat-dev libswscale-dev libxcb-xinerama0

RUN apt-get update && apt-get install -y python-dev python-numpy \
    python3 python3-pip python3-dev libtbb2 libtbb-dev \
    libjpeg-dev libjasper-dev libdc1394-22-dev \
    libopencv-dev ffmpeg python-pycurl \
    libatlas-base-dev gfortran webp qt5-default libvtk6-dev zlib1g-dev

# Project Dependencies
RUN pip3 install opencv-python
RUN pip3 install numpy
RUN pip3 install pygame==2.0.0.dev6
RUN pip3 install matplotlib
RUN pip3 install dlib

RUN cd ~/ &&\
    git clone https://github.com/Itseez/opencv.git &&\
    git clone https://github.com/Itseez/opencv_contrib.git &&\
    cd opencv && mkdir build && cd build && cmake  -DWITH_QT=ON -DWITH_OPENGL=ON -DFORCE_VTK=ON -DWITH_TBB=ON -DWITH_GDAL=ON -DWITH_XINE=ON -DBUILD_EXAMPLES=ON .. && \
    make -j4 && make install && ldconfig && rm -rf ~/opencv*  # Remove the opencv folders to reduce image size

# Set the appropriate link

RUN ln /dev/null /dev/raw1394

CMD ["/bin/bash"]

COPY . ./eyetracking