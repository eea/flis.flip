FROM eeacms/python:2.7-slim

# Copy code into image
RUN mkdir flip
COPY requirements.txt requirements-dev.txt /flip/
WORKDIR flip

# Install requirements
RUN pip install -U setuptools
RUN pip install -r requirements-dev.txt

# Copy code
COPY . /flip
COPY flip/local_settings.py.example flip/local_settings.py
RUN ./manage.py collectstatic --noinput

# Expose needed port
EXPOSE 8001

# Expose static volume
VOLUME ./flip/public/static

#Default command
CMD gunicorn flip.wsgi:application --bind 0.0.0.0:8001
