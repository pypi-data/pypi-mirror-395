..
    Copyright (C) 2020 - 2025 TU Wien.

    Invenio-Theme-TUW is free software; you can redistribute it and/or
    modify it under the terms of the MIT License; see LICENSE file for more
    details.

===================
 Invenio-Theme-TUW
===================

This package belongs to the `TU Wien suite of InvenioRDM customizations <https://gitlab.tuwien.ac.at/crdm>`__ that make up `TU Wien Research Data <https://researchdata.tuwien.ac.at>`__.

It provides various frontend components to give it the distinct look and feel of TU Wien services.
Also, it also brings some extra functionality and new endpoints.



Features
========

Some of the features provided by this package:

* TU Wien corporate design
* Form to contact the owner of records
* Guarded record deposit & community creation pages
* Per-community page with summarized download statistics for its records
* Extra pages with information related to the service at TU Wien (policies, contact, "about" pages, ...)
* Web UI for composing outreach emails to users in the system
* Small bespoke admin pages geared towards use at TU Wien
* Greetings from the Easter Bunny
* Etc.


Even though not strictly a provided feature, the extended testing setup is also noteworthy (see below).



Installation
============

After installing Invenio-Theme-TUW (e.g. via ``pip``), Invenio's assets have to be updated:

.. code-block:: console

   $ pip install invenio-theme-tuw  # or another package manager
   $ invenio-cli assets build



Tests
=====

To execute the tests, the project has to be installed locally.
Then, the ``run-tests.sh`` script can be executed.

.. code-block:: console

   $ uv sync --all-extras
   $ source .venv/bin/activate
   $ ./run-tests.sh
   $ deactivate



Testing setup
-------------

In addition to the usual events like merge requests, the tests are run nightly via GitLab CI/CD.

The definition for the installed environment (``uv.lock``, also exported as ``requirements.txt``) is provided as job artifacts to developers.
This makes it easier to diagnose breakage due to dependency upgrades.

Further, we're checking our overrides (like Jinja templates and JS) against the latest upstream definitions as part of the tests.
In combination with the nightly tests, this provides us with an early warning system about changes that need chasing.
