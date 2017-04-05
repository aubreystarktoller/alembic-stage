=====
About
=====


Installation
============

Supported Python versions are: 2.7, 3.4 and 3.5.

To install using pip:

::

    pip install alembic-stage

You can obtain the source from:

::

    https://github.com/aubreystarktoller/alembic-stage


Usage
=====


Example usage
=============

 
Testing
=======

It is recommend that you use ``make`` and ``tox`` to run the tests. First clone
the git repository and then enter the cloned repository:

::

    git clone https://github.com/aubreystarktoller/alembic-stage
    cd alembic-stage

If you are using ``make`` and ``tox`` to run lint sanity checks and
all tests for all versions of Python use then just invoke ``tox``.

To run the tests in the current environment using ``make`` use ``make test``.

If you're not using ``make``, then to run the tests in the current environment
``setup.py test``.

Coverage
--------

If you have ``make`` and the ``coverage`` package installed code coverage
can be tested by running using ``make coverage``.


Linting
-------

If you have ``make`` and the ``pylint`` package installed a full report
of the code can be generated using ``make lint``.


Authors
=======
* Aubrey Stark-Toller


License
=======
alembic-stage is licensed under the GPL3. See
LICENSE for the full license.
