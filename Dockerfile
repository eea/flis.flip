# Pyhton image

FROM python:2.7-slim

# System requirements

RUN apt-get -y update && apt-get -y install \
    gcc \
    python-setuptools \
    python-dev \
    libxml2-dev \
    libxslt1-dev \
    lib32z1-dev \
    libpq-dev \
    libldap2-dev \
    libsasl2-dev

# Copy code into image

RUN mkdir flis.flip
COPY . /flis.flip
WORKDIR flis.flip

# Install requirements

RUN pip install -U setuptools
RUN pip install -r requirements-dev.txt
COPY flip/local_settings.py.example flip/local_settings.py

# Expose needed port

EXPOSE 8000

#Default command

CMD python ./manage.py runserver 0.0.0.0:8000
