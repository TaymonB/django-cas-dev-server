# django-cas-dev-server
Extends the Django development server to include a local CAS server.

## Dependencies

Requires Django 1.7 or later. Also requires
[django-environ](https://github.com/joke2k/django-environ) and
[MamaCAS](https://github.com/jbittel/django-mama-cas); pip will install these
automatically.

## Installation

Download from the Python Package Index with `pip install django-cas-dev-server`.
Or download the source from GitHub and install with `python setup.py install`.

## Quick Start Guide

1. Install django-cas-dev-server, as explained above.
2. Add the following to the end of your Django project's settings module:

    ```python
    if DEBUG:
        INSTALLED_APPS = ('cas_dev_server',) + INSTALLED_APPS
        CAS_DEV_DATABASE = {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'cas_db.sqlite3',
        }
    ```
3. Set the URL for the CAS server to use in development (for instance,
   `CAS_SERVER_URL` if you're using
   [Django CAS NG](https://github.com/mingchen/django-cas-ng)) to
   `http://localhost:8008/`.
3. Run `python manage.py casdevmanage migrate`.
4. Run `python manage.py casdevmanage createsuperuser` and create a superuser
   at the interactive prompt.
5. Start the development server with `python manage.py runserver`, just like
   always.

## Slightly More Advanced Configuration

django-cas-dev-server provides a pluggable Django app, `cas_dev_server`. This
app has no models or views. Instead, it defines two django-admin commands,
`casdevmanage` and `runserver`, and makes use of one new project setting,
`CAS_DEV_DATABASE`.

`CAS_DEV_DATABASE` should be a configuration dictionary for a database that will
contain the credentials of your CAS users. **This is separate from your Django
project's main database.** Since you're only using it for development, SQLite
should work fine.

`casdevmanage` should be followed by the name of another django-admin command,
along with any legal arguments and/or options for that command. It will run that
command using the settings of the CAS development server, rather than your
project. For instance, `casdevmanage migrate` installs the database tables for
Django's authentication app into the database specified in `CAS_DEV_DATABASE`.

`runserver` overrides the command of the same name from the staticfiles app,
or, if you're not using the staticfiles app, from Django's core set of commands.
It supports two new options in addition to the existing ones:

* `--nocas` disables the CAS development server.
* `--cas-port` specifies which port to run the CAS server on. This needs to be
  different from the port the main development server runs on. By default, port
  8008 is used.

If you're using the staticfiles app, `cas_dev_server` must precede
`django.contrib.staticfiles` in `INSTALLED_APPS` so that django-cas-dev-server's
implementation of `runserver` takes precedence.

When the development server is run, it starts the CAS server in a subprocess.
Logging output from both servers will be visible on the console. The CONTROL-C
keyboard interrupt that stops the development server will also stop the CAS
server.

The CAS server has its own deployment of the Django admin interface, accessible
through the `/admin/` URL (for instance, `http://localhost:8008/admin/`). A
user's permissions level in the CAS database affects whether they can log into
the admin interface; it has no connection with their permissions in your Django
project. (Consequently, you'll probably have to run both `createsuperuser` and
`casdevmanage createsuperuser`, giving the same username to both users, to
ensure that you can log into your main project as a superuser.) After creating
the initial superuser, the easiest way to create additional CAS users is through
the admin interface.
