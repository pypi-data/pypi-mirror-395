""" AccountRequestMetadata api
"""

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

import core_main_app.utils.notifications.mail as send_mail_api
from core_main_app.access_control.api import (
    has_perm_administration,
)
from core_main_app.access_control.decorators import access_control
from core_main_app.commons.exceptions import ApiError
from core_user_registration_app.components.account_request_metadata.models import (
    AccountRequestMetadata,
)
from core_website_app.settings import SERVER_URI


@access_control(has_perm_administration)
def get_all(user):
    """List of opened account requests

    Returns:

        List of all requests
    """
    return AccountRequestMetadata.get_all()


def _get_user_by_username(username):
    """Returns a user given its username

    Args:

        username: Given username

    Returns:

        User
    """
    return User.objects.get(username=username)


def get_account_request_metadata_by_id(account_id):
    """Returns an account Request metadata given its id


    Args:
        account_id:

    Returns:
        AccountRequestMetadata

    """

    return AccountRequestMetadata.get_by_id(account_id)


def _get_user_by_id(user_id):
    """Returns a user given its primary key

    Args:

        user_id: Given user id

    Returns:

        User
    """
    return User.objects.get(pk=user_id)


def insert_metadata(user, account_id, metadata):
    """Insert metadata into RequestAccountMetadata given its id

    Args:
        user
        account_id
        metadata


    """
    # NOTE: used queryset.update to change metadata as assignment would not save change in database
    AccountRequestMetadata.objects.filter(pk=account_id).update(
        metadata=metadata
    )


def create_account_request(user):
    """Create a new request with the metadata

    Args:
        user: Django User

    Returns: New Account request

    """

    try:
        # check if a user with the same username exists
        _get_user_by_username(user.username)
        raise ApiError("A user with the same username already exists.")
    except ObjectDoesNotExist:
        user.save()

        # Create the account request and save it
        account_request = AccountRequestMetadata(
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
        )

        context = {"URI": SERVER_URI}
        template_path = (
            "core_website_app/admin/email/request_account_for_admin.html"
        )
        send_mail_api.send_mail_to_website_contacts(
            subject="New Account Request",
            path_to_template=template_path,
            context=context,
        )
        account_request.save()
        return account_request
