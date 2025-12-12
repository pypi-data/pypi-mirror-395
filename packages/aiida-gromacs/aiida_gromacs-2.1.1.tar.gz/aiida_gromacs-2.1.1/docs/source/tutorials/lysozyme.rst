====================================
Lysozyme in Water with aiida-gromacs
====================================

This tutorial follows Justin Lemkul's `lysozyme <http://www.mdtutorials.com/gmx/lysozyme/>`_ tutorial. We will not explain each individual step as this can be found on Justin's webpage, but we will link to each page and show the AiiDA equivalant command.

.. image:: ../images/lemkul.png
   :width: 400
   :align: center

.. note::
    The tutorial is written with the assumption that you have a working knowledge of GROMACS. If you are new to GROMACS, we recommend following Justin's tutorial first to understand the commands and what they do.

Software requirements
---------------------

For this tutorial, pre-installation of AiiDA, the aiida-gromacs plugin and dependent tools is required, please follow the instructions in the `installation <https://aiida-gromacs.readthedocs.io/en/latest/user_guide/installation.html>`_ section. Here is a brief description of the software used:

* AiiDA uses a `PostgreSQL <https://www.postgresql.org>`_ database to store all data produced and the links between input and output files for each command run. Each submitted command is termed a process in AiiDA.

* Communication between submitted processes are handled with `RabbitMQ <https://www.rabbitmq.com/>`_ and submitted processes are handled with a deamon process that runs in the background.

* ``aiida-gromacs`` requires an installation of `GROMACS <https://www.gromacs.org/>`_ and the path to where it is installed.

This tutorial also assumes yo have the AiiDA tools running in the background, if not please follow the steps `here <https://aiida-gromacs.readthedocs.io/en/latest/user_guide/aiida_sessions.html>`_.

.. note::
    All the files required for this version of the tutorial should be downloaded from `our tutorial files <https://github.com/CCPBioSim/aiida-gromacs/tree/master/examples/lysozyme_files/inputs/>`_ and **not** from the links provided in Justin's tutorial as slight alterations to these files have been made, and those available via Justin's tutorial will cause errors if used here.


"AiiDA-fying" Lemkul's tutorial
-------------------------------

#. We will start from the `pdb2gmx <http://www.mdtutorials.com/gmx/lysozyme/01_pdb2gmx.html>`_ step of Justin's tutorial:

.. code-block:: bash

    gmx_pdb2gmx -f 1AKI_clean.pdb -ff oplsaa -water spce -o 1AKI_forcefield.gro -p 1AKI_topology.top -i 1AKI_restraints.itp

.. note::
    There may be slight differences in commands between the tutorial and that by Justin Lemkul, this is simply down to the way we are recording provenance, which requires non-interactive input into the GROMACS tools.

.. note::
    After each of the steps you should run ``verdi`` to view the status of the submitted process before moving onto the next step, you do this by running:

    .. code-block:: bash

        verdi process list -a

    A successfully finished process will exit with code ``[0]``.

#. Next we will `create the box and solvate <http://www.mdtutorials.com/gmx/lysozyme/03_solvate.html>`_

    Firstly the box:

    .. code-block:: bash

        gmx_editconf -f 1AKI_forcefield.gro -center 0 -d 1.0 -bt cubic -o 1AKI_newbox.gro

    Then solvate:

    .. code-block:: bash

        gmx_solvate -cp 1AKI_newbox.gro -cs spc216.gro -p 1AKI_topology.top -o 1AKI_solvated.gro

#. Add `ions <http://www.mdtutorials.com/gmx/lysozyme/04_ions.html>`_

    Firstly we will use the grompp preprocessor:

    .. code-block:: bash

        gmx_grompp -f ions.mdp -c 1AKI_solvated.gro -p 1AKI_topology.top -o 1AKI_ions.tpr

    Followed by genion:

    .. code-block:: bash

        gmx_genion -s 1AKI_ions.tpr -p 1AKI_topology.top -pname NA -nname CL -neutral true -o 1AKI_solvated_ions.gro


#. Then `minimise <http://www.mdtutorials.com/gmx/lysozyme/05_EM.html>`_ the structure

    Firstly we will use grompp:

    .. code-block:: bash

        gmx_grompp -f min.mdp -c 1AKI_solvated_ions.gro -p 1AKI_topology.top -o 1AKI_minimised.tpr

    Then mdrun to minimise:

    .. code-block:: bash

        gmx_mdrun -s 1AKI_minimised.tpr -c 1AKI_minimised.gro -e 1AKI_minimised.edr -g 1AKI_minimised.log -o 1AKI_minimised.trr

#. Now we will equilibrate with `NVT <http://www.mdtutorials.com/gmx/lysozyme/06_equil.html>`_

    Firstly we will use grompp:

    .. code-block:: bash

        gmx_grompp -f nvt.mdp -c 1AKI_minimised.gro -r 1AKI_minimised.gro -p 1AKI_topology.top -o 1AKI_nvt.tpr

    Then mdrun to equilibrate NVT:

    .. code-block:: bash

        gmx_mdrun -s 1AKI_nvt.tpr -c 1AKI_nvt.gro -e 1AKI_nvt.edr -g 1AKI_nvt.log -cpo 1AKI_nvt.cpt -o 1AKI_nvt.trr

#. Followed by equilibration with `NPT <http://www.mdtutorials.com/gmx/lysozyme/07_equil2.html>`_

    Firstly we will use grompp:

    .. code-block:: bash

        gmx_grompp -f npt.mdp -c 1AKI_nvt.gro -r 1AKI_nvt.gro -t 1AKI_nvt.cpt -p 1AKI_topology.top -o 1AKI_npt.tpr

    Then mdrun to equilibrate NPT:

    .. code-block:: bash

        gmx_mdrun -s 1AKI_npt.tpr -c 1AKI_npt.gro -e 1AKI_npt.edr -g 1AKI_npt.log -cpo 1AKI_npt.cpt -o 1AKI_npt.trr

#. We are now ready for `production <http://www.mdtutorials.com/gmx/lysozyme/08_MD.html>`_ MD.

    Firstly we will use grompp:

    .. code-block:: bash

        gmx_grompp -f prod.mdp -c 1AKI_npt.gro -t 1AKI_npt.cpt -p 1AKI_topology.top -o 1AKI_prod.tpr

    Then mdrun for production run:

    .. code-block:: bash

        gmx_mdrun -s 1AKI_prod.tpr -c 1AKI_production.gro -e 1AKI_production.edr -g 1AKI_production.log -o 1AKI_production.trr

    If running on GPU then something like:

    .. code-block:: bash

        gmx_mdrun -s 1AKI_prod.tpr -c 1AKI_production.gro -e 1AKI_production.edr -g 1AKI_production.log -o 1AKI_production.trr -bonded gpu -nb gpu -pme gpu -ntmpi 1 -ntomp 5 -pin on

That is it! You've ran your first GROMACS simulation with AiiDA.

.. note::
    The majority of the commands used in Justin's tutorial have an equivalent in the ``aiida-gromacs`` plugin. To view all ``gmx`` commands available in the plugin, run:

    .. code-block:: bash

        verdi plugin list aiida.calculations

    Anything starting with ``gromacs.`` is available in the plugin. To use other commands not available in the plugin, you can use the ``genericMD`` CLI, which allows you to save any command you want to keep track of with AiiDA.


Viewing and sharing data
------------------------

You can now view the provenance graph of the simulation by running:

.. code-block:: bash

    verdi node graph generate <PK>

Where ``<PK>`` is the process ID of the last process you ran.

.. note::
    The provenance graph will show all the steps you've taken in the simulation, and the connections between the input and output files for each step. This is a great way to visualise and keep track of your simulations.

The simulation steps can also be viewed on the terminal by running:

.. code-block:: bash

    verdi data provenance show

The provenance can also be archived for sharing with others, to do this run:

.. code-block:: bash

    verdi archive create --all archive_name.aiida

Where ``--all`` saves all the data in the AiiDA profile.

Now, have a go at exploring the AiiDA archive file on a demo database application called  `BioSimDB <https://github.com/CCPBioSim/biosimdb-app>`_. This is a web-based application that allows you to view and store your simulation data provenance in a local database.
