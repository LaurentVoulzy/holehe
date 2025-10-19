FROM python:3.13.9-slim-trixie
COPY . /opt/holehe
WORKDIR /opt/holehe
RUN pip3 install --upgrade pip && \
    pip3 install .
