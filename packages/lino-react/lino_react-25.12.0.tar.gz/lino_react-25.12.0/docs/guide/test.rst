=============
Testing react
=============

We use `jest` and `puppeteer` as javascript testing media.

Python unittest and doctest does NOT cover much of the testing
system and instead rely on javascript packages.

JEST setup
==========

Other then the configuration files, react has four important setup
files in `lino_react/react/testSetup` directory which are as follows::

.. xfile:: lino_react/react/testSetup/setupJEST.js

    Contains initial custom setup for puppeteer browser endpoint and
    runs lino_noi django runserver.

.. xfile:: lino_react/react/testSetup/teardownJEST.js

    Shuts down the lino_noi server and teardown puppeteer endpoint setup.

.. xfile:: lino_react/react/testSetup/testEnvironment.js

    Contains environment setup for each test suite.

.. xfile:: lino_react/react/testSetup/setupTests.ts

    Contains utility functions for test suites used to maintain
    synchronous code executions of each test block.

.. _react.jest.testcommand:

Tests using jest
================

The actual test files are located in the `lino_react/react/components/__tests__`
directory.

The test suites are split into multiple subdirectories, namely `noi` & `avanti`,
for, the test cases depend on a lino server running in the background. We use
lino_noi and lino_avanti as the backend http server on which the test cases are
run. Test cases in subdirectories depend on the application server their name
matches to. The call to `npm test` or any other test related commands depends on
an environment variable `BASE_SITE`. See the examples below on how to run test
cases or suites.

To run the individual test such as the `noi/integrity.ts`,
run the following command (from the root of repository)::

    $ BASE_SITE=noi npm run ntest lino_react/react/components/__tests__/noi/integrity.ts

To run all the test suites, located in `noi` directory, at once, call::

    $ BASE_SITE=noi npm run test

To run all the test suites, located in `avanti` directory, at once, call::

    $ BASE_SITE=avanti npm run test

To run all the test suites at once, call::

    $ ./jest_puppeteer_test.sh
