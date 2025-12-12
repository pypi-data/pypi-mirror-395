""" Unit Test UserMetadata
"""

from core_main_app.commons import exceptions
from core_main_app.settings import DATA_SORTING_FIELDS
from core_main_app.utils.datetime import datetime_now
from core_main_app.utils.integration_tests.integration_base_test_case import (
    IntegrationBaseTestCase,
)
from core_main_app.utils.tests_tools.MockUser import create_mock_user
from core_user_registration_app.components.user_metadata.api import (
    check_xml_file_is_valid,
)
from core_user_registration_app.components.user_metadata.models import (
    UserMetadata,
)
from tests.components.user_metadata.fixtures.fixtures import (
    DataFixtures,
    AccessControlDataFixture,
)

fixture_data = DataFixtures()
access_control_data_fixture = AccessControlDataFixture()


class TestDataGetAll(IntegrationBaseTestCase):

    fixture = access_control_data_fixture

    def test_data_get_all_return_collection_of_data(self):
        # Act
        result = UserMetadata.get_all(DATA_SORTING_FIELDS)
        # Assert
        self.assertTrue(all(isinstance(item, UserMetadata) for item in result))

    def test_data_get_all_return_objects_data_in_collection(self):
        # Act
        result = UserMetadata.get_all(DATA_SORTING_FIELDS)
        # Assert
        self.assertTrue(len(self.fixture.data_collection) == result.count())

    def test_data_get_all_ordering(self):
        # Arrange
        access_control_data_fixture.insert_data()
        ascending_order_by_field = ["+title"]
        descending_order_by_field = ["-title"]
        # Act
        ascending_result = UserMetadata.get_all(ascending_order_by_field)
        descending_result = UserMetadata.get_all(descending_order_by_field)
        # Assert
        for i in range(len(ascending_result)):
            self.assertTrue(
                ascending_result.all()[i].title
                == descending_result.all()[len(ascending_result) - i - 1].title
            )

    def test_data_get_all_ascending_sorting(self):
        # Arrange
        ascending_order_by_field = ["+title"]
        # Act
        ascending_result = UserMetadata.get_all(ascending_order_by_field)
        # Assert
        self.assertTrue(
            self.fixture.data_1.title == ascending_result.all()[0].title
        )
        self.assertTrue(
            self.fixture.data_2.title == ascending_result.all()[1].title
        )

    def test_data_get_all_descending_sorting(self):
        # Arrange
        descending_order_by_field = ["-title"]
        # Act
        descending_result = UserMetadata.get_all(descending_order_by_field)
        # Assert
        self.assertTrue(
            self.fixture.data_2.title
            == descending_result.all()[len(descending_result) - 2].title
        )
        self.assertTrue(
            self.fixture.data_1.title
            == descending_result.all()[len(descending_result) - 1].title
        )

    def test_data_get_all_multi_field_sorting(self):
        # Arrange
        ascending_order_by_multi_field = ["+title", "+user_id"]
        descending_order_by_multi_field = ["+title", "-user_id"]
        # Act
        ascending_result = UserMetadata.get_all(ascending_order_by_multi_field)
        descending_result = UserMetadata.get_all(
            descending_order_by_multi_field
        )
        # Assert
        self.assertEqual(
            self.fixture.data_4.user_id, ascending_result.all()[4].user_id
        )
        self.assertEqual(
            self.fixture.data_5.user_id, ascending_result.all()[3].user_id
        )

        self.assertEqual(
            self.fixture.data_4.user_id, descending_result.all()[3].user_id
        )
        self.assertEqual(
            self.fixture.data_5.user_id, descending_result.all()[4].user_id
        )


class TestDataGetById(IntegrationBaseTestCase):

    fixture = fixture_data

    def test_data_get_by_id_raises_api_error_if_not_found(self):
        # Act # Assert
        with self.assertRaises(exceptions.DoesNotExist):
            UserMetadata.get_by_id(-1)

    def test_data_get_by_id_return_data_if_found(self):
        # Act
        result = UserMetadata.get_by_id(self.fixture.data_1.id)
        # Assert
        self.assertEqual(result, self.fixture.data_1)


def mock_upsert(UserMetadata, user):
    if UserMetadata.xml_content is None:
        raise exceptions.ApiError(
            "Unable to save UserMetadata: xml_content field is not set."
        )

    UserMetadata.last_modification_date = datetime_now()
    check_xml_file_is_valid(UserMetadata)
    return UserMetadata.save()


def _create_user(user_id, is_superuser=False):
    return create_mock_user(user_id, is_superuser=is_superuser)
