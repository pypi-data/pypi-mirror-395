""" Metadata API
"""

from core_main_app.commons import exceptions as exceptions
from core_main_app.utils.datetime import datetime_now
from core_main_app.utils.xml import validate_xml_data
from core_user_registration_app.components.user_metadata.models import (
    UserMetadata,
)
from xml_utils.xsd_tree.xsd_tree import XSDTree


def get_by_id(data_id, user):
    """Return data object with the given id.

    Parameters:
        data_id:
        user:

    Returns: data object
    """
    return UserMetadata.get_by_id(data_id)


def upsert(data, request):
    """Save or update the data.

    Args:
        data:
        user:

    Returns:

    """
    if data.xml_content is None:
        raise exceptions.ApiError(
            "Unable to save data: xml_content field is not set."
        )

    data.last_modification_date = datetime_now()
    check_xml_file_is_valid(data, request=request)
    return data.convert_and_save()


def check_xml_file_is_valid(data, request):
    """Check if xml data is valid against a given schema.

    Args:
        data:
        request:

    Returns:

    """
    template = data.template

    try:
        xml_tree = XSDTree.build_tree(data.xml_content)
    except Exception as e:
        raise exceptions.XMLError(str(e))

    try:
        xsd_tree = XSDTree.build_tree(template.content)
    except Exception as e:
        raise exceptions.XSDError(str(e))
    error = validate_xml_data(xsd_tree, xml_tree, request=request)
    if error is not None:
        raise exceptions.XMLError(error)
    else:
        return True
