.. _installation:

Installation
============

.. contents::
    :local:
    :depth: 1

Install from Conda
------------------

.. warning::

   TODO: Prepare Conda package.

Install from GitHub
-------------------

Check out code from the CliMAF WPS Demo GitHub repo and start the installation:

.. code-block:: sh

   $ git clone https://github.com/cp4cds/climaf-wps-demo.git
   $ cd climafwps
   $ conda env create -f environment.yml
   $ source activate climafwps
   $ python setup.py develop

... or do it the lazy way
+++++++++++++++++++++++++

The previous installation instructions assume you have Anaconda installed.
We provide also a ``Makefile`` to run this installation without additional steps:

.. code-block:: sh

   $ git clone https://github.com/cp4cds/climaf-wps-demo.git
   $ cd climafwps
   $ make clean    # cleans up a previous Conda environment
   $ make install  # installs Conda if necessary and runs the above installation steps

Start CliMAF WPS Demo PyWPS service
-----------------------------------

After successful installation you can start the service using the ``climafwps`` command-line.

.. code-block:: sh

   $ climafwps --help # show help
   $ climafwps start  # start service with default configuration

   OR

   $ climafwps start --daemon # start service as daemon
   loading configuration
   forked process id: 42

The deployed WPS service is by default available on:

http://localhost:5000/wps?service=WPS&version=1.0.0&request=GetCapabilities.

.. NOTE:: Remember the process ID (PID) so you can stop the service with ``kill PID``.

You can find which process uses a given port using the following command (here for port 5000):

.. code-block:: sh

   $ netstat -nlp | grep :5000


Check the log files for errors:

.. code-block:: sh

   $ tail -f  pywps.log

... or do it the lazy way
+++++++++++++++++++++++++

You can also use the ``Makefile`` to start and stop the service:

.. code-block:: sh

  $ make start
  $ make status
  $ tail -f pywps.log
  $ make stop


Run CliMAF WPS Demo as Docker container
---------------------------------------

You can also run CliMAF WPS Demo as a Docker container.

.. warning::

  TODO: Describe Docker container support.

Use Ansible to deploy CliMAF WPS Demo on your System
----------------------------------------------------

Use the `Ansible playbook`_ for PyWPS to deploy CliMAF WPS Demo on your system.


.. _Ansible playbook: http://ansible-wps-playbook.readthedocs.io/en/latest/index.html
