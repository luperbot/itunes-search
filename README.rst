itunes-search
======================================

Overview
--------

Exploring app store metadata.

Installing and Running DynamoDB Local
-------------------------------------

.. code:: bash

    $ brew install dynamodb-local
    $ /usr/local/bin/dynamodb-local

Running Tests
-------------

.. code:: bash

    $ pip install -r requirements.txt
    # Run all tests, including requesting data and loading
    # intial data.
    $ python tests.py
    # Run only tests
    $ python -m unittest tests
