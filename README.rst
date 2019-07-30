StackStorm SDK
==============

|Build Status| |Join our community Slack|

This repository contains different utilities and tools which help with
the StackStorm integration pack development.

Installation
------------

From PyPi (latest stable version):

.. code:: bash

    pip install st2sdk

From git (latest in development version):

.. code:: bash

    pip install -e git+https://github.com/StackStorm/st2sdk.git@master#egg=st2sdk

Tools
-----

Pack Bootstrap / Scaffolding tool
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Pack bootstrap tool makes it easier to get started with the StackStorm
pack development.

Currently, the tool creates the correct pack directory structure.

Usage
^^^^^

Run tool in the non-interactive mode:

.. code:: bash

    st2sdk bootstrap <pack name>

This will create a pack directory named ``<pack name>`` in the current
working directory. This directory will contain all the directories and
files which are needed by pack.

Run tool in the interactive mode:

.. code:: bash

    st2sdk bootstrap -i [pack name]

In the interactive mode, the tool will ask you a couple of questions and
the answers will be used to populate pack metadata and other files.

Check and Lint scripts
~~~~~~~~~~~~~~~~~~~~~~

This repository also contains various “check” and “lint” scripts which
can be ran standalone or hooked up to your continuous integration
system. Those scripts validate metadata file syntax, verify that pack
contains pack.yaml file, etc.

Some of those scripts require access to the database and network
(e.g. PyPi to download pack dependencies, etc.) and they also manipulate
the file system. You should make sure that you provide a clean
environment on every invocation of those scripts. This can be achieved
by using a fresh VM, docker container or similar for each run.

All of those scripts are also hooked up to our Travis CI system and run
on every push to our st2contrib repository.

For some examples on how to utilize this scripts, please refer to the
Makefile in st2contrib repository -
https://github.com/StackStorm/st2contrib/blob/master/Makefile

As you may notice in the Makefile, we have some scripts and
optimizations in place, so by default for Pull Request we only run
scripts on changed files and / or pack. This is an important
optimization because if we ran scripts for all the files and packs (even
the ones which haven’t been touched) this would substantially slow down
the CI run time for a particular Pull Request and delay the time it
takes for user to get feedback about their PR.

In case you have a lot of custom packs in your repository, you might
want to utilize similar approach.

st2-check-validate-yaml-file
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This script verifies that a provided YAML file contains a valid syntax.
It’s usually used with action metadata files and other YAML files.

Usage:

.. code:: bash

    st2-check-validate-yaml-file <path to YAML file>

Keep in mind that this script just performs syntax and no semantic
checks. If you want to confirm that your action or other metadata file
is correct, you should also run ``st2-check-register-pack-resources``
script which tries to register all the resources in a pack and errors
out of registration

st2-check-validate-json-file
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This script verified that a provided JSON file contains a valid syntax. It's
usually used with action metadata files and other YAML files.

Usage:

.. code:: bash

    st2-check-validate-json-file <path to JSON file>

Keep in mind that this script just performs syntax and no semantic checks. If
you want to confirm that your action or other metadata file is correct, you
should also run ``st2-check-register-pack-resources`` script which tries to register
all the resources in a pack and errors out of registration of a particular
resource fails.

st2-check-validate-pack-metadata-exists
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
This script verifies that a pack contains ``pack.yaml`` metadata file.

Usage:

.. code:: bash

    st2-check-validate-pack-metadata-exists <path to the pack root directory>

st2-check-register-pack-resources
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This script tries to register all the resources in a particular pack and fails
if registering a particular resource fails.

Usage:

.. code:: bash

    st2-check-register-pack-resources <path to the pack root directory>

This script requires access to a fresh database (MongoDB) on each run. In
addition to that, it requires all the StackStorm components (st2actions,
st2common, etc.) to be in ``PYTHONPATH``. You can achieve that by cloning st2
repository in a particular directly (e.g. ``/tmp/st2``) and then setting
``ST2_REPO_PATH`` environment variable to point to that directory when invoking
the script.

st2-check-pylint-pack
^^^^^^^^^^^^^^^^^^^^^

This script runs ``pylint`` on all the Python files inside a particular pack.

Usage:

.. code:: bash

    st2-check-pylint-pack <path to the pack root directory>

This script installs packs regular and test requirements so it needs to run
inside a virtual environment which is created for purpose of this script.

Similar to ``st2-check-register-pack-resources`` this script also requires
access to StackStorm code-base and st2 components. You can achieve that by
cloning st2 repository in a particular directly (e.g. ``/tmp/st2``) and then
setting ``ST2_REPO_PATH`` environment variable to point to that directory when
invoking the script.

st2-check-print-pack-tests-coverage
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This script prints a test coverage for a particular pack. It prints all the
actions which contains tests and the ones which are missing it.

Keep in mind that this script is for informational purposes only - right now
it doesn't fail if some action is missing tests.

Usage:

.. code:: bash

    st2-check-print-pack-tests-coverage <path to the pack root directory>

Copyright, License, and Contributors Agreement
----------------------------------------------

Copyright 2019 StackStorm, Inc.

Licensed under the Apache License, Version 2.0 (the “License”); you may
not use this work except in compliance with the License. You may obtain
a copy of the License in the `LICENSE`_ file, or at:

http://www.apache.org/licenses/LICENSE-2.0

By contributing you agree that these contributions are your own (or
approved by your employer) and you grant a full, complete, irrevocable
copyright license to all users and developers of the project, present
and future, pursuant to the license of the project.

.. |Build Status| image:: https://circleci.com/gh/StackStorm/st2sdk/tree/master.svg?style=shield
   :target: https://circleci.com/gh/StackStorm/st2sdk
.. |Join our community Slack| image:: https://stackstorm-community.herokuapp.com/badge.svg
   :target: https://stackstorm.com/community-signup
.. _LICENSE: LICENSE
