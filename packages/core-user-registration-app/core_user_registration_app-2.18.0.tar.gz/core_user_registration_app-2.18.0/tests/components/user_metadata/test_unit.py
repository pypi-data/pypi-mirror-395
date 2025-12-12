""" Unit tests for UserMetada components
"""

from unittest import TestCase
from unittest.mock import Mock, patch, MagicMock

from django.test import override_settings

from core_main_app.commons.exceptions import ApiError
from core_user_registration_app.components.user_metadata.api import upsert
from core_user_registration_app.components.user_metadata.models import (
    UserMetadata,
)


class TestUpsert(TestCase):
    """Tests api upsert function"""

    def setUp(self) -> None:
        """setUp"""
        self.data = Mock()

    def test_xml_content_none_raise_api_error(self):
        """test_xml_content_none_raise_api_error"""
        self.data.xml_content = None

        with self.assertRaises(ApiError):
            upsert(self.data, None)

    @patch(
        "core_user_registration_app.components.user_metadata.api.check_xml_file_is_valid"
    )
    def test_xml_content_present_saves_data(
        self, mock_check_xml_file_is_valid
    ):
        """test_xml_content_present_saves_data"""
        mock_check_xml_file_is_valid.return_value = None
        self.data.xml_content = "mock_xml_content"

        upsert(self.data, None)
        self.assertTrue(self.data.convert_and_save.called)


class TestUserMetadata(TestCase):
    """Test User Metadata"""

    @patch("core_main_app.utils.xml.raw_xml_to_dict")
    def test_user_metadata_convert_to_dict_converts_xml(
        self, mock_raw_xml_to_dict
    ):
        """test_user_metadata_convert_to_dict_converts_xml"""

        # Arrange
        user_metadata = _create_user_metadata()

        # Act
        user_metadata.convert_to_dict()

        # Assert
        self.assertTrue(mock_raw_xml_to_dict.called)

    @override_settings(MONGODB_INDEXING=True)
    @patch("core_main_app.utils.xml.raw_xml_to_dict")
    def test_user_metadata_convert_to_dict_not_converted_xml_when_mongodb(
        self, mock_raw_xml_to_dict
    ):
        """test_user_metadata_convert_to_dict_not_converted_xml_when_mongodb"""

        # Arrange
        user_metadata = _create_user_metadata()

        # Act
        user_metadata.convert_to_dict()

        # Assert
        self.assertFalse(mock_raw_xml_to_dict.called)

    def test_user_metadata_convert_to_file_converts_xml(
        self,
    ):
        """test_user_metadata_convert_to_dict_converts_xml"""

        # Arrange
        user_metadata = _create_user_metadata()

        # Act
        user_metadata.convert_to_file()

        # Assert
        self.assertEqual(
            user_metadata.file.read().decode(), user_metadata.content
        )

    @patch("django.core.files.uploadedfile.SimpleUploadedFile.__init__")
    def test_user_metadata_convert_to_file_with_encode_error(
        self, mock_simple_upload_file
    ):
        """test_user_metadata_convert_to_file_with_encode_error"""

        # Arrange
        user_metadata = _create_user_metadata()
        mock_content = MagicMock()
        mock_content.encode.side_effect = UnicodeEncodeError("", "", 0, 0, "")
        user_metadata.content = mock_content
        mock_simple_upload_file.return_value = None

        # Act
        user_metadata.convert_to_file()

        # Assert
        self.assertTrue(mock_simple_upload_file.called)
        self.assertTrue(mock_content.encode)


def _create_user_metadata():
    """Create User Metadata

    Returns:

    """
    user_metadata = UserMetadata()
    user_metadata.title = "title"
    user_metadata.xml_content = "<root></root>"
    return user_metadata
