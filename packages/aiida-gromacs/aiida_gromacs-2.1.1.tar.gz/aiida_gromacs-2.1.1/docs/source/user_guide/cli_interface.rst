=========================
Plugin on the Commandline
=========================

Before attempting to use the features here, you need to have completed the steps in :doc:`installation` and started the verdi daemon as described in :doc:`aiida_sessions`.

With our plugin, we are aiming for as simple a transition to using these tools as is possible, so the design philosophy we have chosen is to attempt to mimmick as much as is possible the functionality of native gromacs CLI tools. We currently support the following set of commandline tools and their full feature set. We also have implemented a :doc:`../tutorials/genericMD` interface to provide support for features that we currently do not have, or newly released in the gromacs application.

It is through this powerful interface that you will be able to build powerful workflows or use data provenance capturing tools in this plugin in your existing ways of working without cultural change in the way that you work!

The following utilities are available and have the following features.

gmx_editconf
++++++++++++

Our plugin introduces a new CLI program utility that supports all of the commandline functionality of the original ``editconf`` executable listed `here <https://manual.gromacs.org/current/onlinehelp/gmx-editconf.html>`__

If the original command is used like this:

.. code-block:: bash

    gmx editconf -f 1AKI_forcefield.gro -center 0 -d 1.0 -bt cubic -o 1AKI_newbox.gro

Then in our plugin, you would use it like this:

.. code-block:: bash

    gmx_editconf -f 1AKI_forcefield.gro -center 0 -d 1.0 -bt cubic -o 1AKI_newbox.gro

This utility has extra functionality, such as if you run the command with --help then it will print out comprehensive documentation for usage. There are also two commandline flags for controlling AiiDA parameters that are not native to gromacs. These are:

* --code  -  This allows you to specify different gromacs installs, either local or remote or different versions
* --description  -  This allows you to specify a short description of the command operation for metadata, you should provide this in quotes on the commandline.

An example specifying gromacs on the local PC is below:

.. code-block:: bash

    gmx_editconf --code gmx@localhost -f 1AKI_forcefield.gro -center 0 -d 1.0 -bt cubic -o 1AKI_newbox.gro

gmx_genion
++++++++++

Our plugin introduces a new CLI program utility that supports all of the commandline functionality of the original ``genion`` executable listed `here <https://manual.gromacs.org/current/onlinehelp/gmx-genion.html>`__

If the original command is used like this:

.. code-block:: bash

    gmx genion -s 1AKI_ions.tpr -p 1AKI_topology.top -pname NA -nname CL -neutral true -o 1AKI_solvated_ions.gro

Then in our plugin, you would use it like this:

.. code-block:: bash

    gmx_genion -s 1AKI_ions.tpr -p 1AKI_topology.top -pname NA -nname CL -neutral true -o 1AKI_solvated_ions.gro

This utility has extra functionality, such as if you run the command with --help then it will print out comprehensive documentation for usage. There are also two commandline flags for controlling AiiDA parameters that are not native to gromacs. These are:

* --code  -  This allows you to specify different gromacs installs, either local or remote or different versions
* --description  -  This allows you to specify a short description of the command operation for metadata, you should provide this in quotes on the commandline.
* --instructions  -  This allows you to specify a file that contains the instructions for the ``genion`` command. This is a file that contains the commands that you would normally type into the ``genion`` commandline. This is a file that is read in by the plugin and executed as if you had typed it into the commandline.

An example specifying gromacs on the local PC is below:

.. code-block:: bash

    gmx_genion --code gmx@localhost -s 1AKI_ions.tpr -p 1AKI_topology.top -pname NA -nname CL -neutral true -o 1AKI_solvated_ions.gro

gmx_grompp
++++++++++

Our plugin introduces a new CLI program utility that supports all of the commandline functionality of the original ``grompp`` executable listed `here <https://manual.gromacs.org/current/onlinehelp/gmx-grompp.html>`__

If the original command is used like this:

.. code-block:: bash

    gmx grompp -f ions.mdp -c 1AKI_solvated.gro -p 1AKI_topology.top -o 1AKI_ions.tpr

Then in our plugin, you would use it like this:

.. code-block:: bash

    gmx_grompp -f ions.mdp -c 1AKI_solvated.gro -p 1AKI_topology.top -o 1AKI_ions.tpr

This utility has extra functionality, such as if you run the command with --help then it will print out comprehensive documentation for usage. There are also two commandline flags for controlling AiiDA parameters that are not native to gromacs. These are:

* --code  -  This allows you to specify different gromacs installs, either local or remote or different versions
* --description  -  This allows you to specify a short description of the command operation for metadata, you should provide this in quotes on the commandline.

An example specifying gromacs on the local PC is below:

.. code-block:: bash

    gmx_grompp --code gmx@localhost -f ions.mdp -c 1AKI_solvated.gro -p 1AKI_topology.top -o 1AKI_ions.tpr

gmx_mdrun
+++++++++

Our plugin introduces a new CLI program utility that supports all of the commandline functionality of the original ``mdrun`` executable listed `here <https://manual.gromacs.org/current/onlinehelp/gmx-mdrun.html>`__

If the original command is used like this:

.. code-block:: bash

    gmx mdrun -s 1AKI_em.tpr -c 1AKI_minimised.gro -e 1AKI_minimised.edr -g 1AKI_minimised.log -o 1AKI_minimised.trr

Then in our plugin, you would use it like this:

.. code-block:: bash

    gmx_mdrun -s 1AKI_em.tpr -c 1AKI_minimised.gro -e 1AKI_minimised.edr -g 1AKI_minimised.log -o 1AKI_minimised.trr

This utility has extra functionality, such as if you run the command with --help then it will print out comprehensive documentation for usage. There are also two commandline flags for controlling AiiDA parameters that are not native to gromacs. These are:

* --code  -  This allows you to specify different gromacs installs, either local or remote or different versions
* --description  -  This allows you to specify a short description of the command operation for metadata, you should provide this in quotes on the commandline.

An example specifying gromacs on the local PC is below:

.. code-block:: bash

    gmx_mdrun --code gmx@localhost -s 1AKI_em.tpr -c 1AKI_minimised.gro -e 1AKI_minimised.edr -g 1AKI_minimised.log -o 1AKI_minimised.trr

gmx_pdb2gmx
+++++++++++

Our plugin introduces a new CLI program utility that supports all of the commandline functionality of the original ``pdb2gmx`` executable listed `here <https://manual.gromacs.org/current/onlinehelp/gmx-pdb2gmx.html>`__

If the original command is used like this:

.. code-block:: bash

    gmx pdb2gmx -f 1AKI_clean.pdb -ff oplsaa -water spce -o 1AKI_forcefield.gro -p 1AKI_topology.top -i 1AKI_restraints.itp

Then in our plugin, you would use it like this:

.. code-block:: bash

    gmx_pdb2gmx -f 1AKI_clean.pdb -ff oplsaa -water spce -o 1AKI_forcefield.gro -p 1AKI_topology.top -i 1AKI_restraints.itp

This utility has extra functionality, such as if you run the command with --help then it will print out comprehensive documentation for usage. There are also two commandline flags for controlling AiiDA parameters that are not native to gromacs. These are:

* --code  -  This allows you to specify different gromacs installs, either local or remote or different versions
* --description  -  This allows you to specify a short description of the command operation for metadata, you should provide this in quotes on the commandline.

An example specifying gromacs on the local PC is below:

.. code-block:: bash

    gmx_pdb2gmx --code gmx@localhost -f 1AKI_clean.pdb -ff oplsaa -water spce -o 1AKI_forcefield.gro -p 1AKI_topology.top -i 1AKI_restraints.itp

gmx_solvate
+++++++++++

Our plugin introduces a new CLI program utility that supports all of the commandline functionality of the original ``solvate`` executable listed `here <https://manual.gromacs.org/current/onlinehelp/gmx-solvate.html>`__

If the original command is used like this:

.. code-block:: bash

    gmx solvate -cp 1AKI_newbox.gro -cs spc216.gro -p 1AKI_topology.top -o 1AKI_solvated.gro

Then in our plugin, you would use it like this:

.. code-block:: bash

    gmx_solvate -cp 1AKI_newbox.gro -cs spc216.gro -p 1AKI_topology.top -o 1AKI_solvated.gro

This utility has extra functionality, such as if you run the command with --help then it will print out comprehensive documentation for usage. There are also two commandline flags for controlling AiiDA parameters that are not native to gromacs. These are:

* --code  -  This allows you to specify different gromacs installs, either local or remote or different versions
* --description  -  This allows you to specify a short description of the command operation for metadata, you should provide this in quotes on the commandline.

An example specifying gromacs on the local PC is below:

.. code-block:: bash

    gmx_solvate --code gmx@localhost -cp 1AKI_newbox.gro -cs spc216.gro -p 1AKI_topology.top -o 1AKI_solvated.gro


gmx_make_ndx
++++++++++++

Our plugin introduces a new CLI program utility that supports all of the commandline functionality of the original ``make_ndx`` executable listed `here <https://manual.gromacs.org/current/onlinehelp/gmx-make_ndx.html>`__

If the original command is used like this:

.. code-block:: bash

    gmx make_ndx -f 1AKI_minimised.gro -o index.ndx

Then in our plugin, you would use it like this:

.. code-block:: bash

    gmx_make_ndx -f 1AKI_minimised.gro -o index.ndx --instructions inputs.txt

This utility has extra functionality, such as if you run the command with --help then it will print out comprehensive documentation for usage. There are also three commandline flags for controlling AiiDA parameters that are not native to gromacs. These are:

* --code  -  This allows you to specify different gromacs installs, either local or remote or different versions
* --description  -  This allows you to specify a short description of the command operation for metadata, you should provide this in quotes on the commandline.
* --instructions  -  This allows you to specify a file that contains the instructions for the ``make_ndx`` command. This is a file that contains the commands that you would normally type into the ``make_ndx`` commandline. This is a file that is read in by the plugin and executed as if you had typed it into the commandline.

An example specifying gromacs on the local PC is below:

.. code-block:: bash

    gmx_make_ndx --code gmx@localhost -f 1AKI_minimised.gro -o index.ndx --instructions inputs.txt
