FROM java:8
ENV LANG=en_US.UTF-8
ENV PYTHONIOENCODING=utf8
RUN apt-get update
# Install python
RUN apt-get install -y gcc make python-dev libxml2-dev libxslt-dev gzip
RUN curl -s https://bootstrap.pypa.io/get-pip.py | python
# Install pygrib dependencies manually
RUN apt-get install -y libgrib-api-dev && pip install numpy==1.10.1 pyproj==1.9.4
# Add files
WORKDIR /home/
ADD . /home/
RUN make install
CMD make server