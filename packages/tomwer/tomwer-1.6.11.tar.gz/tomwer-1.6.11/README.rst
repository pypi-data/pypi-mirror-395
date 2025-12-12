.. image:: doc/img/tomwer.png
   :alt: Tomwer Logo
   :align: left
   :width: 400px

Introduction
------------

**Tomwer** provides tools to automate acquisition and reconstruction processes for tomography. The package includes:

- A library to individually access each acquisition process.
- Graphical User Interface (GUI) applications to control key processes such as reconstruction and data transfer, which can be executed as standalone applications.
- An Orange add-on to help users define custom workflows (`Orange3 <http://orange.biolab.si>`_).

Tomwer relies on `Nabu <https://gitlab.esrf.fr/tomotools/nabu>`_ for tomographic reconstruction.

**Note**: Currently, the software is only compatible with Linux.

Documentation
-------------

The latest version of the documentation is available `here <https://tomotools.gitlab-pages.esrf.fr/tomwer/>`_.

Installation
------------

Step 1: Installing Tomwer
'''''''''''''''''''''''''

To install Tomwer with all features:

.. code-block:: bash

    pip install tomwer[full]

Alternatively, you can install the latest development branch from the repository:

.. code-block:: bash

    pip install git+https://gitlab.esrf.fr/tomotools/tomwer/#egg=tomwer[full]


Step 2: (Optional) Update Orange-CANVAS-CORE and Orange-WIDGET-BASE
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

If you need access to additional 'processing' wheels and 'reprocess action,' you may want to update these Orange forks. This is optional, as the project works with the native Orange libraries.

.. code-block:: bash

    pip install git+https://github.com/payno/orange-canvas-core --no-deps --upgrade
    pip install git+https://github.com/payno/orange-widget-base --no-deps --upgrade


Launching Applications
-----------------------

After installation, Tomwer includes several applications. You can launch an application by running:

.. code-block:: bash

    tomwer <appName> [options]

- If you run `tomwer` without arguments, a manual page will be displayed.
- For application-specific help, run:

.. code-block:: bash

    tomwer <appName> --help


Tomwer Canvas - Orange Canvas
-----------------------------

You can launch the Orange canvas to create workflows using the available building blocks:

.. code-block:: bash

    tomwer canvas

- Alternatively, you can use `orange-canvas`.
- If you're using a virtual environment, remember to activate it:

.. code-block:: bash

    source myvirtualenv/bin/activate


Building Documentation
-----------------------

To build the documentation:

.. code-block:: bash

    sphinx-build doc build/html

The documentation will be generated in `doc/build/html`, and the entry point is `index.html`. To view the documentation in a browser:

.. code-block:: bash

    firefox build/html/index.html

**Note**: Building the documentation requires `sphinx` to be installed, which is not a hard dependency of Tomwer. If needed, install it separately.
