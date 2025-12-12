A shared library for dataset inventory and asdf generation.
-----------------------------------------------------------

|codecov|

Running Tests
-------------

At the start of the pytest run the test suite calls the simulator to generate a number of test datasets (with small array size).
This process takes some time, when quickly iterating on test failures this can be annoying.
To share the simulated data over multiple test runs invoke the test suite with the ``--cached-tmpdir=/path/`` argument.
This will use the specified path for all simulated datasets and not regenerate if the files are already present.
**Note**: It is up to you to make sure the files are correct and to remove all the files if they need to change.

License
-------

This project is Copyright (c) NSO / AURA and licensed under
the terms of the BSD 3-Clause license. This package is based upon
the `Openastronomy packaging guide <https://github.com/OpenAstronomy/packaging-guide>`_
which is licensed under the BSD 3-clause licence. See the licenses folder for
more information.

.. |codecov| image:: https://codecov.io/bb/dkistdc/dkist-inventory/graph/badge.svg?token=K0EIXHFQ04
   :target: https://codecov.io/bb/dkistdc/dkist-inventory
