""" System api to access data without access control neither API rules
"""

from core_main_app.components.template.models import Template
from core_main_app.components.version_manager.utils import (
    get_latest_version_name,
)
from core_main_app.utils.xml import is_schema_valid, get_hash
from core_parser_app.components.data_structure.models import (
    DataStructureElement,
)
from core_user_registration_app.components.user_template_version_manager.models import (
    UserTemplateVersionManager,
)


def insert_registry_user_schema(xsd_filename, xsd_content):
    # Check if schema is valid
    is_schema_valid(xsd_content)
    template = Template(
        filename=xsd_filename, _hash=get_hash(xsd_content), content=xsd_content
    )
    template.save_template()

    # save the template in database
    try:
        user_version_manager = UserTemplateVersionManager(
            title=xsd_filename, is_default=True
        )
        user_version_manager.save_version_manager()
        # insert the initial template in the version manager
        template.version_manager = user_version_manager
        # set current version
        if len(user_version_manager.versions) == 0:
            template.is_current = True
        # update saved template
        template.display_name = get_latest_version_name(user_version_manager)
        # save template
        template.save()
        # return version manager
        return user_version_manager, template
    except Exception as e:
        template.delete()
        raise e


def get_all_data_structure_elements():
    """Returns all data structure elements"""
    return DataStructureElement.objects.all()


def get_active_global_version_manager_by_title(version_manager_title):
    """Return all active Version Managers with user set to None.

    Args:
        version_manager_title:

    Returns:

    """
    return (
        UserTemplateVersionManager.get_active_global_version_manager_by_title(
            version_manager_title
        )
    )
