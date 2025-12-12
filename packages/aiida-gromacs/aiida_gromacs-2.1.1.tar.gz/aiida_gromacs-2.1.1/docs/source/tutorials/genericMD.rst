=============
genericMD CLI
=============

Sometimes, you may want to track commands outside of GROMACS. The genericMD CLI allows you to keep track of these commands directly from the aiida-gromacs plugin installation.

GROMACS specific vs genericMD CLI process submissions
-----------------------------------------------------

First let's take a look at what a process submitted using a gromacs specific CLI command compares with submitting the job with the genericMD CLI:

Submitting a ``pdb2gmx`` process using ``gmx_pdb2gmx``:

.. code-block:: bash

    gmx_pdb2gmx -f 1AKI_clean.pdb -ff oplsaa -water spce -o 1AKI_forcefield.gro -p 1AKI_topology.top -i 1AKI_restraints.itp

Submitting the equivalent process with ``genericMD``

.. code-block:: bash

    genericMD --code gmx@localhost \
    --command "pdb2gmx -i 1AKI_restraints.itp -o 1AKI_forcefield.gro -p 1AKI_topology.top -ff oplsaa -water spce -f 1AKI_clean.pdb" \
    --inputs path/to/1AKI_clean.pdb \
    --outputs 1AKI_restraints.itp --outputs 1AKI_topology.top --outputs 1AKI_forcefield.gro

As you can see, using the genericMD CLI is more verbose, but it does allow for submitting any command you want to keep track of with AiiDA.

.. note::
    The quoted command text for the ``--command`` flag does not need to include the path to the input files, instead you include the paths to files in the ``--inputs`` flag.

.. note::
    By default, the outputs produced from the command are returned to the current working directory. To change where the output files are returned, set the full path with the ``--output_dir`` flag.


How to submit a process with genericMD
--------------------------------------

To submit an AiiDA process for tracking input and output files of a generic command, there are several things you need to know beforehand:

#. what the full command you want to run is,
#. where is the program you're using in your command installed,
#. what are the input file names you're using in the command,
#. and what are the output file names outputted from your command.

Once you know this information, you can build a genericMD process submission. Let's take a look at the example below for a submission for tracking the inputs and outputs of a ``diff`` command:

.. code-block:: bash

    genericMD --code bash@localhost --command "diff file1.txt file2.txt > out.txt" --inputs file1.txt --inputs file2.txt --outputs out.txt

Here,

#. the command we want to run is ``diff file1.txt file2.txt > out.txt``, which is specified with the ``--command`` flag and wrapped in quotation marks
#. the diff utility is installed on the local computer and can be run via bash, this is communicated to AiiDA with ``--code bash@localhost``
#. each input file used in the diff command needs to be explicitly defined using the ``--inputs`` flag, this allows for AiiDA to keep track of these files
#. similarly for the output files, use the ``--outputs`` flag to define each output from the command, which allows AiiDA to track these files

A few things to consider when using genericMD, firstly the inputs and ouputs of a command need to be known before submitting the process.

.. warning::
    Any inputs/outputs not included in the genericMD submission with ``--inputs`` and ``--outputs`` flags repectively, will not be included as a node in the provenance graph!



Another example to submit a process with genericMD
--------------------------------------------------

The example above for tracking the ``diff`` command may be useful for tracking changes to files made on non-command line based programs, for example when using a GUI to add or delete atoms in a ``.pdb`` file. Here's another example for tracking a command outside of GROMACS using `Packmol <https://m3g.github.io/packmol/userguide.shtml>`_ to create the initial system geometry for MD simulations.

First, we add the packmol code:

.. code-block:: bash

    verdi code create core.code.installed --label packmol --computer localhost --filepath-executable ~/packmol-20.14.2/packmol

.. code-block:: console

        Report: enter ? for help.
        Report: enter ! to ignore the default and set no value.
        Description: Initial configurations for Molecular Dynamics Simulations by packing optimization
        Default `CalcJob` plugin: genericMD
        Escape using double quotes [y/N]: y
        Success: Created InstalledCode<3>

This assumes that Packmol is already installed on your computer in the path ``~/packmol-20.14.2/packmol``, if not then follow the Packmol installation guide or follow the summarised guide below.

#. `Download <http://m3g.iqm.unicamp.br/packmol>`_ the ``packmol-20.13.0.tar.gz`` file
#.  Expand the files with ``tar -xvzf packmol-20.13.0.tar.gz``
#.  Build the executable with ``cd packmol; make``

You can check the Packmol code is added with:

.. code-block:: bash

    verdi code list

.. code-block:: console

        Full label           Pk  Entry point
        -----------------  ----  -------------------
        gmx@localhost         1  core.code
        bash@localhost        2  core.code
        packmol@localhost     3  core.code.installed

Once the Packmol is added as a code, we can track a Packmol code with the ``genericMD`` calculation with:

.. code-block:: bash

    genericMD --code packmol@localhost --command "< packmol.inp" \
    --inputs path/to/packmol.inp --inputs path/to/input.pdb \
    --outputs path/to/output.pdb

That's it, you can track a command from code installed on your computer external to GROMACS.
