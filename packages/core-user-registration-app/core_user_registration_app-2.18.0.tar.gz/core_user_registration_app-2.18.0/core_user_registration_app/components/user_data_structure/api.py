""" User data Structure api
"""

from core_main_app.access_control.api import has_perm_administration
from core_main_app.access_control.decorators import access_control
from core_user_registration_app.access_control.api import (
    can_read,
    can_change_owner,
)
from core_user_registration_app.components.user_data_structure.models import (
    UserDataStructure,
)


def upsert(user_data_structure, user):
    """Save or update the user Data Structure

    Args:
        user_data_structure:
        user:

    Returns:

    """
    return user_data_structure.save_object()


@access_control(has_perm_administration)
def get_all(user):
    """Returns all user data structure api

    Returns:

    """
    return UserDataStructure.get_all()


def get_by_id(user_data_structure_id):
    """Returns the user data structure with the given id

    Args:
        user_data_structure_id:
        user:

    Returns:

    """
    return UserDataStructure.get_by_id(user_data_structure_id)


def delete(user_data_structure, user):
    """Deletes the user data structure and the element associated

    Args:
        user_data_structure:
        user:
    """
    user_data_structure.delete_data_structure_with_elements()


@access_control(can_read)
def get_by_data_id(data_id, user):
    """Return the user data structure with the given data id

    Args:
        data_id:

    Returns:

    """
    return UserDataStructure.get_by_data_id(data_id)


def update_data_structure_root(user_data_structure, root_element, user):
    """Update the data structure with a root element.

    Args:
        user_data_structure:
        root_element:

    Returns:

    """
    # Delete data structure elements
    user_data_structure.delete_data_structure_elements_from_root()

    # set the root element in the data structure
    user_data_structure.data_structure_element_root = root_element

    # save the data structure
    return upsert(user_data_structure, user)


@access_control(can_read)
def get_by_data_structure_element_root_id(data_structure_element_root, user):
    """Return the user data structure with the given data structure element root id

    Args:
        data_structure_element_root:
        user:

    Returns:

    """
    return UserDataStructure.get_by_data_structure_element_root(
        data_structure_element_root
    )


@access_control(can_change_owner)
def change_owner(user_data_structure, new_user, user):
    """Change user data structure's owner.

    Args:
        user_data_structure:
        user:
        new_user:

    Returns:
    """
    user_data_structure.user = str(new_user.id)
    user_data_structure.save_object()
