"""Registration models
"""

from django.db import models

from core_main_app.permissions.utils import get_formatted_name
from core_user_registration_app.permissions import rights


class Register(models.Model):
    class Meta(object):
        verbose_name = "core_user_registration_app"
        default_permissions = ()
        permissions = (
            (
                rights.register_access,
                get_formatted_name(rights.register_access),
            ),
            (
                rights.register_data_structure_access,
                get_formatted_name(rights.register_data_structure_access),
            ),
        )
