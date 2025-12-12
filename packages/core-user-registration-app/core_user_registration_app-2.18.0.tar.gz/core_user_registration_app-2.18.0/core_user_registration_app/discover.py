""" Initialize permissions for core user registration app.
"""

import logging
from os.path import join

from django.contrib.auth.models import Group, Permission
from django.contrib.staticfiles import finders
from django.core.exceptions import ObjectDoesNotExist
from django.db.migrations.exceptions import BadMigrationError
from django_celery_beat.models import CrontabSchedule, PeriodicTask

import core_main_app.permissions.rights as main_rights
import core_user_registration_app.permissions.rights as registration_rights
from core_main_app.commons import exceptions
from core_main_app.components.template_xsl_rendering import (
    api as template_xsl_rendering_api,
)
from core_main_app.components.xsl_transformation import (
    api as xslt_transformation_api,
)
from core_main_app.components.xsl_transformation.models import (
    XslTransformation,
)
from core_main_app.utils import file as file_utils
from core_user_registration_app import settings as user_registration_settings
from core_user_registration_app.components.user_template_version_manager.models import (
    UserTemplateVersionManager,
)
from core_user_registration_app.system import api as registry_system_api
from core_user_registration_app.tasks import delete_user_data_structure

logger = logging.getLogger(__name__)


def init_registration_app():
    """Init the registry. Add the registry template.

    Returns:

    """
    # Check if data were previously inserted
    if UserTemplateVersionManager.objects.count() > 0:
        logger.warning("The database is not empty. Skipping migration.")
        return

    # Check if settings are set
    if (
        not user_registration_settings.REGISTRY_XSD_USER_FILEPATH
        or not user_registration_settings.REGISTRY_XSD_USER_FILENAME
        or not user_registration_settings.XSL_FOLDER_PATH
        or not user_registration_settings.LIST_XSL_FILENAME
        or not user_registration_settings.DETAIL_XSL_FILENAME
    ):
        raise BadMigrationError(
            "Please configure the REGISTRY_XSD_USER_FILENAME "
            "and REGISTRY_XSD_USER_FILEPATH, "
            "XSL_FOLDER_PATH, LIST_XSL_FILENAME and DETAIL_XSL_FILENAME "
            "setting in your project."
        )

    # Load files
    default_xsd_path = finders.find(
        user_registration_settings.REGISTRY_XSD_USER_FILEPATH
    )
    list_xslt_path = finders.find(
        join(
            user_registration_settings.XSL_FOLDER_PATH,
            user_registration_settings.LIST_XSL_FILENAME,
        )
    )
    detail_xslt_path = finders.find(
        join(
            user_registration_settings.XSL_FOLDER_PATH,
            user_registration_settings.DETAIL_XSL_FILENAME,
        )
    )
    if not default_xsd_path or not list_xslt_path or not detail_xslt_path:
        raise BadMigrationError(
            "A file required for loading data was not found."
        )

    # Read files
    xsd_data = file_utils.read_file_content(default_xsd_path)

    # Create User template
    (
        user_template_vm,
        current_version,
    ) = registry_system_api.insert_registry_user_schema(
        user_registration_settings.REGISTRY_XSD_USER_FILENAME, xsd_data
    )
    # Save list and detail XSLT
    list_xslt = _get_or_create_xslt(
        list_xslt_path, user_registration_settings.LIST_XSL_FILENAME
    )
    detail_xslt = _get_or_create_xslt(
        detail_xslt_path, user_registration_settings.DETAIL_XSL_FILENAME
    )

    # Bind XSLT to template
    template_xsl_rendering_api.add_or_delete(
        template=current_version,
        list_xslt=list_xslt,
        default_detail_xslt=detail_xslt,
        list_detail_xslt=[detail_xslt],
    )


def init_permissions():
    """Initialization of groups and permissions."""
    try:
        # Get or Create the default group
        anonymous, created = Group.objects.get_or_create(
            name=main_rights.ANONYMOUS_GROUP
        )

        # Get registration permissions
        register_access_perm = Permission.objects.get(
            codename=registration_rights.register_access
        )
        register_view_data_save_repo_perm = Permission.objects.get(
            codename=registration_rights.register_data_structure_access
        )

        # Add permissions to default group
        anonymous.permissions.add(
            register_access_perm,
            register_view_data_save_repo_perm,
        )

    except Exception as e:
        logger.error("Impossible to init register permissions: %s" % str(e))


def _get_or_create_xslt(file_path, filename):
    """Get or create a xslt.

    Args:
        file_path: XSLT filename.

    Returns:
        XSLT.

    """
    try:
        return xslt_transformation_api.get_by_name(filename)
    except exceptions.DoesNotExist:
        logger.info(f"XSLT {filename} not found, creating it now.")
        # Read content.
        xsl_data = file_utils.read_file_content(file_path)
        # Create the XSLT.
        list_xslt = XslTransformation(
            name=filename, filename=filename, content=xsl_data
        )
        return xslt_transformation_api.upsert(list_xslt)


def init_periodic_tasks():
    """Create periodic tasks for the app and add them to a crontab schedule"""
    schedule, _ = CrontabSchedule.objects.get_or_create(
        minute="*",
    )
    try:
        PeriodicTask.objects.get(name=delete_user_data_structure.__name__)
    except ObjectDoesNotExist:
        PeriodicTask.objects.create(
            crontab=schedule,
            name=delete_user_data_structure.__name__,
            task="core_user_registration_app.tasks.delete_user_data_structure",
        )
