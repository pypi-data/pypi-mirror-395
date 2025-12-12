.. _getting_started:

Quick start
===========

To run this python package it is recommended to first create a virtual environment using virtualenv or conda.
The package can then be installed through:

>>> pip install trap

Once installed you should have access to the command line utilities ``trap-run`` and ``trap-view``.
The former is for processing the images and creating a database with sources. The latter is a debug
utility for visualizing the data in the expored databsae.

>>> trap-run --help
>>> trap-view --help

The parameters used by TraP are stored in a .toml configuration file.
The default file can be found here:
https://git.astron.nl/RD/trap/-/blob/main/trap_config.toml?ref_type=heads

These parameters can be modified either in that file or via the command line, e.g. ``trap-run --detection-threshold=5``.
You can use command-line parameters to override settings in the configuration file, because they take precedence.

If the configuration file is not found by TraP, you can point to it by

>>> trap-run --config_file /path/to/config/file

By default TraP will look for the configuration file in the folder where you are running.
Specifying the location of the config file is also handy if you have several versions
of the configuration in the folder and you want to use one of your presets.

The input files can be supplied using ``--input_images`` or ``-i``.
This can refer to either a file, directory or glob pattern (e.g. 'images/my_image_*.fits').
When using a glob pattern, remember to wrap the line in quotes or the terminal might get confused.
If a directory or glob pattern is used, all fits images found there will be used.
If a nested directory is supplied, the subdirectories will also be searched for fits files.
These arguments can be supplied multiple times to refer to multiple files or locations.
An example is:

>>> trap-run -i images/day1/ -i images/day3/specific_file.fits -i 'images/day2/some_other_*_files.fits'

The result will be a combination of all images of day1, and a subset of the images in day2 that match the \*
pattern and the specific file from day 3. The fits files will be sorted on observation start time so the order
in which they are supplied does not matter.

Using multiple CPU cores
------------------------
TraP uses Dask to process multiple images at once.
This significantly speeds up the code. For more information on this,
see the input parameters ``--nr_threads`` and ``--scheduler``.

For more information on these arguments, see :ref:`Input arguments <input_arguments>`

.. Warning ::

    By default Dask will use as many threads as there are CPU cores.
    Depending on your setup, this can cause TraP to read in too many
    images at once, causing the RAM to overflow. When this happens the
    program often crashes after a few seconds with a 'Killed' error or
    something similar. If this happens, reduce the number of cores used
    by setting --nr_threads yourself.

Viewing a progress dashboard
----------------------------
When the ``--scheduler=distributed`` setting is used, a dashboard is created.
This dashboard shows information on the progess and resource usage.
The location of the dashboard is printed to the terminal at the start of the run,
but the default location is http://127.0.0.1:8787/status.
If you run TraP on a different machine, you have to either connect to that machine
with a VNC and open the url in a browser in the VNC, or you can create a tunnel
such that you can view it on the browser on your own machine.
Creating a tunnel on ubuntu usually looks something like: ``ssh -L 8787:localhost:8787 -N user@machine.server.com``
Here I mapped port 8787 on my machine to that of the other machine. If this does not work for you,
check the TraP stdout logs (terminal output) for the port used on the machine it was running on.

.. Note ::

    The dashboard is only live while the program is running

..
