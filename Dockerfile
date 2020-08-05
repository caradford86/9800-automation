FROM python:3.8.3-slim-buster

LABEL maintainer="chris.radford@wwt.com"

WORKDIR /wlc

ENV PYTHONUNBUFFERED='true'
ENV DEBIAN_FRONTEND=noninteractive

# Install Linux packages
RUN apt-get update \
    && apt-get install -qq -y \
               build-essential \
               git \
               libpq-dev --no-install-recommends

COPY . /wlc

# Install Python Packages
RUN pip install -r /wlc/requirements.txt

EXPOSE 8000

CMD ["/bin/bash"]