""" Apps file for setting core package when app is ready
"""

import sys

from django.apps import AppConfig


class UserRegistrationAppConfig(AppConfig):
    """Core application settings."""

    name = "core_user_registration_app"
    verbose_name = "Core User Registration App"

    def ready(self):
        """Run when the app is ready.

        Returns:

        """
        if "migrate" not in sys.argv:
            import core_user_registration_app.discover as discover

            discover.init_permissions()
