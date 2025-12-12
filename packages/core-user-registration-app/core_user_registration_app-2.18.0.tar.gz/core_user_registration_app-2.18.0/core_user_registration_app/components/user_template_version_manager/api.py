"""
User Version Manager API
"""

from core_main_app.access_control.decorators import access_control
from core_main_app.commons.exceptions import CoreError
from core_main_app.components.template import api as template_api
from core_main_app.components.template.access_control import can_read_global
from core_main_app.components.version_manager import api as version_manager_api
from core_main_app.components.version_manager.utils import (
    get_latest_version_name,
)
from core_main_app.utils.file import get_file_extension
from core_user_registration_app.components.user_template_version_manager.access_control import (
    can_write,
)
from core_user_registration_app.components.user_template_version_manager.models import (
    UserTemplateVersionManager,
)


@access_control(can_write)
def insert(user_version_manager, template, request):
    """Add a version to a user template version manager.

    Args:
        user_version_manager:
        template:
        request:

    Returns:

    """
    template_extension = get_file_extension(template.filename)
    if template_extension != ".xsd":
        raise CoreError("Unsupported user registration template format.")
    # save the template in database
    template_api.upsert(template, request=request)
    try:
        # create a version manager
        version_manager_api.upsert(user_version_manager, request=request)
        # set version manager
        template.version_manager = user_version_manager
        # set current version
        if len(user_version_manager.versions) == 0:
            template.is_current = True
        # update template
        template.display_name = get_latest_version_name(user_version_manager)
        # save template
        template.save_template()
        # return version manager
        return user_version_manager
    except Exception as e:
        template.delete()
        raise e


@access_control(can_read_global)
def get_global_version_managers(request, _cls=True):
    """Get all global version managers of a template.

    Args:
        request:
        _cls:

    Returns:

    """
    return UserTemplateVersionManager.get_global_version_managers(_cls)


def get_version_manager_by_id(id):
    """Return Version manager with given version manager id

    Args:
        id:

    Returns:

    """
    return UserTemplateVersionManager.get_by_id(id)


def get_default_version_manager():
    """Return default User Version Manager.

    Returns:

    """
    return UserTemplateVersionManager.objects.filter(is_default=True)


@access_control(can_write)
def upsert(user_version_manager, request):
    """Save or update user_version manager.

    Args:
        user_version_manager:
        request:

    Returns:

    """
    user_version_manager.save_version_manager()


def set_default_version_manager(user_version_manager, request):
    """Set default version manager.

    Args:
        user_version_manager:
        request:

    Returns:

    """
    default_user_version_manager = (
        UserTemplateVersionManager.get_default_version_manager()
    )
    for version_manager in default_user_version_manager:
        version_manager.is_default = False
        version_manager.save_version_manager()
    user_version_manager = get_version_manager_by_id(user_version_manager)
    user_version_manager.is_default = True
    user_version_manager.save_version_manager()

    return user_version_manager
