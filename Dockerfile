FROM eeacms/python:2.7-slim

# Copy code into image
RUN mkdir flip
COPY requirements.txt requirements-dev.txt /flip/
WORKDIR flip

# Install requirements
RUN apt-get -y install cron \
 && pip install -U setuptools \
 && pip install -r requirements-dev.txt

# Copy code
COPY . /flip
COPY flip/local_settings.py.docker flip/local_settings.py

# Expose needed port
EXPOSE 8001

# Expose static volume
VOLUME /flip/public/static

#Default command
CMD ["./docker-entrypoint.sh"]
