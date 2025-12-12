core_user_registration_app
==========================

User registration module for the core project.

Quick start
===========

1. Add "core_user_registration_app" to your INSTALLED_APPS setting
------------------------------------------------------------------

.. code:: python

    INSTALLED_APPS = [
      ...
      'core_user_registration_app',
    ]

2. Include the core_user_registration_app URLconf in your project urls.py
-------------------------------------------------------------------------

.. code:: python

    re_path(r'^', include('core_user_registration_app.urls')),