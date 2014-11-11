FLIP
====

Project Name
------------
FLIP - Forward Looking Information in Policy making.


Install dependencies
--------------------
We should use Virtualenv for isolated environments. The following commands will
be run as an unprivileged user in the product directory::

1. Clone the repository::

    git clone https://github.com/eea/flis.flip.git

2. Create & activate a virtual environment::

    virtualenv --no-site-packages sandbox
    echo '*' > sandbox/.gitignore
    source sandbox/bin/activate

3. Install dependencies::

    pip install -r requirements-dev.txt

4. Create a configuration file::

    cd flip
    cp local_settings.py.example local_settings.py

5. Set up the Postgres database::

    To set up the PostgreSQL database in Debian, you need to install the
    packages `postgresql-9.1`, `postgresql-contrib-9.1` and
    `postgresql-server-dev-9.1`. Then create a database and grant access to your user.

    root # su - postgres
    postgres $ psql template1
    psql (9.1.2)
    Type "help" for help.

    template1=# CREATE USER <your username> WITH PASSWORD '<password>';
    CREATE ROLE
    template1=# CREATE DATABASE flip;
    CREATE DATABASE
    template1=# GRANT ALL PRIVILEGES ON DATABASE flip TO <your username>;
    GRANT
    template1=# \q

6. Sync and migrate the database::

    ./manage.py syncdb
    ./manage.py migrate

7. Load fixtures::

    ./manage.py loadfixtures
    ./manage.py load_metadata_fixtures


Create a migration after changes in models.py
---------------------------------------------
::
    ./manage.py schemamigration flip --auto
    ./manage.py migrate
