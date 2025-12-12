====================
AiiDA CLI Cheatsheet
====================

Here we will list some useful commands for working with AiiDA. Have a look `here <https://aiida.readthedocs.io/projects/aiida-core/en/latest/reference/command_line.html?highlight=verdi%20process%20list>`_ to explore all available AiiDA command line subcommands.

Monitoring Submitted Processes
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

List all submitted processes::

    verdi process list -a

Delete a process node, identified by its primary key value ``<PK>``::

    verdi node delete <PK>

Delete multiple process nodes between primary key values ``<PK_1>`` and ``<PK_n>``::

    verdi node delete {<PK_1>..<PK_n>}

View all the nodes associated with a process node::

    verdi node show <PK>

View attributes of a process node (such as retrieved files and find the path on disk where outputs are stored temporarily)::

    verdi node attributes <PK>

From the node attributes output dictionary, you can find where the input and output files are temporarily stored for a process in the "remote_workdir" value.

Visualise Data Provenance
^^^^^^^^^^^^^^^^^^^^^^^^^

Visualise your submitted jobs as a provenance graph outputted in a ``.pdf`` file. Select the latest ``<PK>`` to include all previous nodes in the graph::

    verdi node graph generate <PK>


Debugging
^^^^^^^^^

Any aiida errors are logged in ``.aiida/daemon/log/``.

If any changes to the plugin code are made, after an update for example, restart the daemon if it is already running to implement the code changes::

    verdi daemon restart --reset

Sharing Data
^^^^^^^^^^^^

When you are ready to share data, the AiiDA database and accompanying files inputted and outputted in each process can be `archived <https://aiida.readthedocs.io/projects/aiida-core/en/latest/howto/share_data.html>`_ into a single file::

    verdi archive create --all archive_name.aiida

where the ``--all`` flag saves all the data in the AiiDA profile. To import an existing AiiDA archive file to a loaded profile::

    verdi archive import archive_name.aiida


Plugin Specfic AiiDA Commands
+++++++++++++++++++++++++++++

The following commands are only available with the aiida-amber plugin.

Show Provenance on CLI
^^^^^^^^^^^^^^^^^^^^^^

Show a list of the commands run and the connected inputs/outputs associated with any processes that have been run using::

    verdi provenance show
