:orphan:

.. _trap_database:

TraP database
-------------

For a complete overview of the export database structure, see the section :ref:`database reference <database_reference>`.

Data export
===========

TraP stores its results in a database. This database is created and managed by TraP and should
be regarded as the export product. After the database is created the database can be handled like any
other database, meaning that it can be queried, copied, modified etc., depending on the settings of the
system of course.

.. Warning ::

    TraP writes to the databases not only after processing, but also during.
    Any data during that time is likely incomplete. It is especially recommended
    to avoid any write operations not managed by TraP.

..

The results stored in the database are generally made up of the sources
found in each image and their parameters, as well as indices linking those sources together.
From this information, lightcurves can be constructed. For a complete overview of the tables stored
in the database, refer to the :ref:`database reference <database_reference>`.

For examples on how to use the database for extracting interesting data to visualize,
see the examples in the :ref:`example gallery <example_gallery>`

PostgreSQL vs SQLite
====================
TraP supports both PostgreSQL and SQLite as database backends. Which database to use is up to the user's preference
and likely depends on the server configuration.

SQLite is a lightweight database in the form of a file. SQL queries can be made like in a standard
relational database. The nature of the database being a file makes it very easy to move and distribute.

PostgreSQL is a common database to use on a server. It is robust and allows extended configurations
regarding which users are allowed to view or modify which databases.

Appending to the database
=========================
It is intended to allow for a TraP run to add to an existing database.
New sources will be appended and association indices will be updated.
TraP should be able to read the sources from the database and re-create the source-list
such that it can associate the new sources to those already in the database.
Appending to the database should work for either backend.
This functionality is planned but not yet implemented.

Common gotchas
==============

**db_name**

The '--db_name' parameter behaves differently depending on the backend. If a PostgreSQL database
is used as a backend, this parameter refers to the name of the database.
If a SQLite backend is used, this refers to the path to the sqlite file.

**Overwriting the database**

To prevent accidental removal of data, TraP throws an error if the database already exists.
If this is deliberate and you want to wipe and replace the database, use the **--db_overwrite** option.
That option will remove the existing database and start a new one. This happens for either backend.

**PostgreSQL settings**

The SQLite backend only needs a `--db_name` to run, but PostgreSQL requires more configuration.
Make sure that:

 - the user you are using has the correct write privileges
 - the correct user, password, hostname and port are supplied
 - no passwords are stored in the config file, especially if others can access it. Use the '--db_password' command line argument.

.. Note ::

    While the configuration parameters are stored in the config table in the export database,
    the 'db_password' is not stored to prevent credentials from leaking when the database is
    shared with others.
