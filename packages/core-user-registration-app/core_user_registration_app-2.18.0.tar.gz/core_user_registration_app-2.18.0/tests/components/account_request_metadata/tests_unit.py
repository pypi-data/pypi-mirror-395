""" Tests of the account request API
"""

from unittest.case import TestCase

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from unittest.mock import Mock, patch

from core_main_app.commons.exceptions import ApiError
from core_user_registration_app.components.account_request_metadata import (
    api as account_request_metadata_api,
)
from core_user_registration_app.components.account_request_metadata.models import (
    AccountRequestMetadata,
)


class TestsAccountRequestMetadataGet(TestCase):
    @patch(
        "core_user_registration_app.components.account_request_metadata.api.get_account_request_metadata_by_id"
    )
    def test_account_request_metadata_get_return_request_object(
        self, mock_get_by_id
    ):
        # Arrange
        request_id = "1"
        mock_get_by_id.return_value = _create_account_request_metadata()
        # Act
        result = (
            account_request_metadata_api.get_account_request_metadata_by_id(
                request_id
            )
        )
        # Assert
        self.assertIsInstance(result, AccountRequestMetadata)


class TestsAccountRequestMetadataInsert(TestCase):
    def setUp(self):
        self.mock_account_request_metadata = _create_account_request_metadata()

    @patch(
        "core_user_registration_app.components.account_request_metadata.api._get_user_by_username"
    )
    def test_account_request_metadata_insert_raise_ApiError_if_username_already_exist(
        self, mock_get_user_by_username
    ):
        # Arrange
        mock_user = Mock(spec=User)
        mock_user.username = "username"
        mock_get_user_by_username.return_value = mock_user

        # Act # Assert
        with self.assertRaises(ApiError):
            account_request_metadata_api.create_account_request(mock_user)

    @patch(
        "core_user_registration_app.components.account_request_metadata.models.AccountRequestMetadata.save"
    )
    @patch(
        "core_user_registration_app.components.account_request_metadata.api._get_user_by_username"
    )
    def test_account_request_metadata_insert_return_request(
        self, mock_get_user_by_username, mock_save
    ):
        # Arrange
        mock_user = Mock(spec=User)
        mock_user.username = "username"
        mock_get_user_by_username.side_effect = ObjectDoesNotExist()
        mock_save.return_value = self.mock_account_request_metadata

        # Act
        result = account_request_metadata_api.create_account_request(mock_user)

        # Assert
        self.assertIsInstance(result, AccountRequestMetadata)


def _create_account_request_metadata(username="username"):
    """
    Create an AccountRequestMetadata object using default parameters

    Parameters:
        username (str):

    Returns:
        AccountRequestMetadata object
    """
    return AccountRequestMetadata(username=username)
