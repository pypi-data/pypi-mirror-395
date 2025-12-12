================
Start/Stop AiiDA
================

Regardless of whether you have switched off AiiDA or restarted your computer. To start recording provenance with this plugin, you will need to start up your AiiDA instance. Likewise, once you have finished using AiiDA, it is best practice to shut things down gracefully. These steps also assume you have already followed the steps within :doc:`installation` and have already a fully working install of the toolchain.

The first step in starting AiiDA is to activate your conda environment, for example:

.. code-block:: bash

    conda activate aiida-2.4.0

Initialising the AiiDA database
+++++++++++++++++++++++++++++++

If this is the first time you are using AiiDA, then initialise your AiiDA database:

.. code-block:: bash

    initdb -D ~/.aiida/aiida_db

This creates a directory called ``~/.aiida``, where data created via AiiDA is stored.

Starting AiiDA
++++++++++++++

The next step is to start the AiiDA database:

.. code-block:: bash

    pg_ctl -D ~/.aiida/aiida_db -l ~/.aiida/logfile start
    rabbitmq-server -detached

Then start the AiiDA process daemon:

.. code-block:: bash

    verdi daemon start 2

You can then confirm all is well by checking the status of verdi:

.. code-block:: bash

    verdi status

.. _create-profile-label:

Creating an AiiDA Database Profile
++++++++++++++++++++++++++++++++++

To start using AiiDA-amber to track the inputs and outputs of Amber commands, AiiDA first requires for a profile to be set up for each project via verdi. Verdi is the command line tool in AiiDA used to interact with the AiiDA database. All commands run via the aiida-amber plugin are tracked and stored in the AiiDA database. `Create a profile <https://aiida.readthedocs.io/projects/aiida-core/en/latest/howto/installation.html?highlight=quicksetup#creating-profiles>`_  within the AiiDA database:

.. code-block:: bash

    verdi quicksetup
        Info: enter "?" for help
        Info: enter "!" to ignore the default and set no value
        Profile name: username
        Email Address (for sharing data): your@email.com
        First name: Your
        Last name: Name
        Institution: where-you-work


That is it, you are now free to use your AiiDA toolchain.

Stopping AiiDA
++++++++++++++

It is best to stop your AiiDA instance gracefully than to simply close your VM or shutdown your computer, this protects against any issues that might corrupt your database.

Firstly stop the verdi process daemon:

.. code-block:: bash

    verdi daemon stop

Next stop the database process:

.. code-block:: bash

    pg_ctl -D ~/.aiida/aiida_db stop
    rabbitmqctl stop

Finally you can deactivate your conda environment:

.. code-block:: bash

    conda deactivate

That is it, you now have fully disabled the AiiDA toolchain.


Switching AiiDA Database Profile
++++++++++++++++++++++++++++++++

If you are working on multiple projects, you can create a :ref:`new profile <create-profile-label>` as before and view all created profiles:

.. code-block:: bash

    verdi profile list

If you want to switch to a different ``<PROFILE>``:

.. code-block:: bash

    verdi profile setdefault <PROFILE>

And to delete a profile no longer needed:

.. code-block:: bash

    verdi profile delete <PROFILE>

You can now create, switch and delete profiles saved in the AiiDA database.
