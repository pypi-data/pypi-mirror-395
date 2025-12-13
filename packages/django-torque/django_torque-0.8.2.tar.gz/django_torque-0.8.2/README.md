# The torque app

This is the django app that should be deployed in a running django server.

Outside of installing the app, this should remain a black box.  The reason being
that none of the routes or uses for this should be accessed except
through the [Torque MediaWiki plugin](https://www.mediawiki.org/wiki/Extension:Torque).

For developers, look in the individual code files for details on the inner
workings.

See [INSTALL.md](https://code.librehq.com/ots/mediawiki/torque/-/blob/main/django-torque/INSTALL.md) for installation instructions.

# Django Commands

torque ships commands

## remove_unattached

Whenever loading up a new collection, there may be changes to the form of the data
as the collection evolves.  Because it may be uploaded in mistake, nothing is deleted
from the database to ensure that no unintentional data loss occurs.  However, admins
may want to remove that data to reflect the upgrades in the data.

`remove_unattached` removes those items.  Each field/document that gets uploaded will
be marked as `attached`.  If there are edits associated with a field or document, then
the `--forced` argument is required.

## run_cache_rebuilder

`run_cache_rebuilder` starts up the cache rebuilder.  This is responsible for all
the cache regeneration, and split off to a separate application in order to ensure
that it doesn't affect the main process.  It IS required to run, though, as it
does important database upkeep items as part of it's workflow.

If you want to run it as part of the application instead of separately, add
`"torque.cache_rebuilder",` as an `INSTALLED_APP` in your settings file, as
is exampled in [test_settings.py](test_settings.py) and [INSTALL.md](INSTALL.md)

## Removing attachment files

As a system runs, old FileField files can hang around on the hard drive.  Those
are usually uploaded attachments and templates.  This can start to take up
too much space.  To remove, one was is to use
[https://github.com/akolpakov/django-unused-media](django-unused-media):

```
$ pipenv install django-unused-media
```

Add `'django_unused_media'` to your INSTALLED_APPS and then run:

```
$ pipenv run python ./manage.py cleanup_unused_media
```
