""" Unit Test User Data Structure
"""

from unittest.case import TestCase

from unittest.mock import patch

import core_user_registration_app.components.user_data_structure.api as user_data_structure_api
from core_main_app.commons import exceptions
from core_main_app.components.template.models import Template
from core_main_app.utils.tests_tools.MockUser import create_mock_user
from core_user_registration_app.components.user_data_structure.models import (
    UserDataStructure,
)


class TestUserDataStructureGetById(TestCase):
    @patch.object(UserDataStructure, "get_by_id")
    def test_user_data_structure_get_by_id_raises_does_not_exist_error_if_not_found(
        self, mock_get
    ):

        # Arrange
        mock_get.side_effect = exceptions.DoesNotExist("")

        # Act # Assert
        with self.assertRaises(exceptions.DoesNotExist):
            user_data_structure_api.get_by_id(1)

    def test_data_structure_get_by_id_raises_doesnotexist_if_not_found(self):

        # Act # Assert
        with self.assertRaises(exceptions.DoesNotExist):
            user_data_structure_api.get_by_id(1)

    @patch.object(UserDataStructure, "get_by_id")
    def test_user_data_structure_get_by_id_return_data_if_found(
        self, mock_get
    ):
        # Arrange
        mock_data_structure = UserDataStructure(
            user="1", template=Template(), name="name"
        )
        mock_get.return_value = mock_data_structure
        # Act
        result = user_data_structure_api.get_by_id(1)
        # Assert
        self.assertIsInstance(result, UserDataStructure)


class TestUserDataStructureUpsert(TestCase):
    @patch.object(UserDataStructure, "save_object")
    def test_user_data_structure_upsert_return_data_structure_element(
        self, mock_save
    ):
        # Arrange
        mock_data_structure = UserDataStructure(
            user="1", template=Template(), name="name"
        )
        mock_save.return_value = mock_data_structure
        mock_user = create_mock_user("1")
        # Act
        result = user_data_structure_api.upsert(mock_data_structure, mock_user)
        # Assert
        self.assertIsInstance(result, UserDataStructure)


class TestUserDataStructureGetAll(TestCase):
    @patch.object(UserDataStructure, "get_all")
    def test_user_data_get_all_return_collection_of_user_data(self, mock_list):
        # Arrange
        mock_data_1 = UserDataStructure(
            user="1", template=_get_template(), name="name_title_1"
        )
        mock_data_2 = UserDataStructure(
            user="1", template=_get_template(), name="name_title_2"
        )
        mock_list.return_value = [mock_data_1, mock_data_2]
        # Act
        result = user_data_structure_api.get_all(
            create_mock_user("1", is_staff=True, is_superuser=True)
        )
        # Assert
        self.assertTrue(
            all(isinstance(item, UserDataStructure) for item in result)
        )


def _get_template():
    template = Template()
    template.id_field = 1
    xsd = (
        '<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">'
        '<xs:element name="tag"></xs:element></xs:schema>'
    )
    template.content = xsd
    return template
