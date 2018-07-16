.. _configuration:

Configuration
=============

Command-line options
--------------------

You can overwrite the default `PyWPS`_ configuration by using command-line options.
See the CliMAF WPS Demo help which options are available::

    $ climafwps start --help
    --hostname HOSTNAME        hostname in PyWPS configuration.
    --port PORT                port in PyWPS configuration.

Start service with different hostname and port::

    $ climafwps start --hostname localhost --port 5001

Use a custom configuration file
-------------------------------

You can overwrite the default `PyWPS`_ configuration by providing your own
PyWPS configuration file (just modifiy the options you want to change).
Use one of the existing ``sample-*.cfg`` files as example and copy them to ``etc/custom.cfg``.

For example change the hostname (*localhost*) and the path to the CMIP5 data archive:

.. code-block:: sh

   $ cd climafwps
   $ vim etc/custom.cfg
   $ cat etc/custom.cfg
   [server]
   url = http://localhost:5000/wps
   outputurl = http://localhost:5000/outputs

   [logging]
   level = INFO

   [data]
   archive_root = /data/cmip5/data

Start the service with your custom configuration:

.. code-block:: sh

   # start the service with this configuration
   $ climafwps start -c etc/custom.cfg


.. _PyWPS: http://pywps.org/
