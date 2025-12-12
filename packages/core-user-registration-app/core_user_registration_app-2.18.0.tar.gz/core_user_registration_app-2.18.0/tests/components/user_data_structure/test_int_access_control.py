""" ACL Test Data Structure
"""

from django.contrib.auth.models import AnonymousUser

import core_user_registration_app.components.user_data_structure.api as user_data_structure_api
from core_main_app.access_control.exceptions import AccessControlError
from core_main_app.utils.integration_tests.integration_base_test_case import (
    IntegrationBaseTestCase,
)
from core_main_app.utils.tests_tools.MockUser import create_mock_user
from core_parser_app.components.data_structure.models import (
    DataStructureElement,
)
from core_user_registration_app.components.user_data_structure.models import (
    UserDataStructure,
)
from tests.components.user_data_structure.fixtures.fixtures import (
    UserDataStructureFixtures,
)

fixture_data_structure = UserDataStructureFixtures()


class TestUserDataStructureGetAll(IntegrationBaseTestCase):
    fixture = fixture_data_structure

    def test_get_all_as_superuser_returns_all_data_structure(self):
        mock_user = create_mock_user("1", is_staff=True, is_superuser=True)
        result = user_data_structure_api.get_all(mock_user)
        self.assertTrue(
            all(isinstance(item, UserDataStructure) for item in result)
        )

    def test_get_all_as_user_raises_error(self):
        mock_user = create_mock_user("1")
        with self.assertRaises(AccessControlError):
            user_data_structure_api.get_all(mock_user)

    def test_get_all_as_anonymous_user_raises_error(self):
        with self.assertRaises(AccessControlError):
            user_data_structure_api.get_all(AnonymousUser())


class TestUserDataStructureDelete(IntegrationBaseTestCase):
    fixture = fixture_data_structure

    def test_delete_others_data_structure_as_superuser_deletes_data_structure(
        self,
    ):
        data_structure = self.fixture.data_structure_3
        mock_user = create_mock_user(
            self.fixture.data_structure_1.user,
            is_staff=True,
            is_superuser=True,
        )
        user_data_structure_api.delete(data_structure, mock_user)

    def test_delete_own_data_structure_deletes_data_structure(self):
        data_structure = self.fixture.data_structure_1
        mock_user = create_mock_user(self.fixture.data_structure_1.user)
        user_data_structure_api.delete(data_structure, mock_user)


class TestUserDataStructureUpdateDataStructureRoot(IntegrationBaseTestCase):
    fixture = fixture_data_structure

    def test_update_others_data_structure_root_as_superuser_updates_data_structure(
        self,
    ):
        data_structure = self.fixture.data_structure_1
        new_data_structure_element_root = DataStructureElement()
        new_data_structure_element_root.save()
        mock_user = create_mock_user(
            self.fixture.data_structure_2.user,
            is_staff=True,
            is_superuser=True,
        )
        user_data_structure_api.update_data_structure_root(
            data_structure, new_data_structure_element_root, mock_user
        )
        result = user_data_structure_api.get_by_id(data_structure.id)
        self.assertTrue(isinstance(result, UserDataStructure))
        self.assertTrue(
            result.data_structure_element_root, new_data_structure_element_root
        )

    def test_update_own_data_structure_root_updates_data_structure(self):
        data_structure = self.fixture.data_structure_1
        new_data_structure_element_root = DataStructureElement()
        new_data_structure_element_root.save()
        mock_user = create_mock_user(self.fixture.data_structure_1.user)
        user_data_structure_api.update_data_structure_root(
            data_structure, new_data_structure_element_root, mock_user
        )
        result = user_data_structure_api.get_by_id(data_structure.id)
        self.assertTrue(isinstance(result, UserDataStructure))
        self.assertTrue(
            result.data_structure_element_root, new_data_structure_element_root
        )


class TestUserDataStructureCreateOrUpdate(IntegrationBaseTestCase):
    fixture = fixture_data_structure

    def test_upsert_own_data_structure_updates_data_structure(self):
        data_structure = self.fixture.data_structure_1
        data_structure.name = "new_name_1"
        mock_user = create_mock_user(self.fixture.data_structure_1.user)
        user_data_structure_api.upsert(data_structure, mock_user)
        result = user_data_structure_api.get_by_id(data_structure.id)
        self.assertTrue(isinstance(result, UserDataStructure))
        self.assertTrue(data_structure.name, result.name)


class TestUserDataStructureGetByDataId(IntegrationBaseTestCase):
    fixture = fixture_data_structure

    def test_get_by_data_id_as_superuser_returns_data_structure(self):

        mock_user = create_mock_user(
            self.fixture.data_structure_3.user,
            is_staff=True,
            is_superuser=True,
        )
        data_structure = user_data_structure_api.get_by_data_id(
            self.fixture.data.id, mock_user
        )
        self.assertTrue(isinstance(data_structure, UserDataStructure))
        self.assertEqual(self.fixture.data.id, data_structure.data.id)

    def test_get_by_data_id_as_owner_returns_data_structure(self):
        mock_user = create_mock_user(self.fixture.data_structure_1.user)
        data_structure = user_data_structure_api.get_by_data_id(
            self.fixture.data.id, mock_user
        )
        self.assertTrue(isinstance(data_structure, UserDataStructure))
        self.assertEqual(self.fixture.data.id, data_structure.data.id)

    def test_get_by_data_id_as_user_non_owner_raises_error(self):
        mock_user = create_mock_user(self.fixture.data_structure_3.user)
        with self.assertRaises(AccessControlError):
            user_data_structure_api.get_by_data_id(
                self.fixture.data.id, mock_user
            )

    def test_get_by_data_id_as_anonymous_user_raises_error(self):
        with self.assertRaises(AccessControlError):
            user_data_structure_api.get_by_data_id(
                self.fixture.data.id, AnonymousUser()
            )


class TestDataStructureChangeOwner(IntegrationBaseTestCase):

    fixture = fixture_data_structure

    def test_change_owner_from_owner_to_owner_ok(self):
        mock_owner = create_mock_user(self.fixture.data_structure_1.user)
        user_data_structure_api.change_owner(
            document=fixture_data_structure.data_structure_1,
            new_user=mock_owner,
            user=mock_owner,
        )

    def test_change_owner_from_owner_to_user_ok(self):
        mock_owner = create_mock_user(self.fixture.data_structure_1.user)
        mock_user = create_mock_user("2")
        user_data_structure_api.change_owner(
            document=fixture_data_structure.data_structure_1,
            new_user=mock_user,
            user=mock_owner,
        )

    def test_change_owner_from_user_to_user_raises_exception(self):
        mock_owner = create_mock_user("0")
        mock_user = create_mock_user("2")
        with self.assertRaises(AccessControlError):
            user_data_structure_api.change_owner(
                document=fixture_data_structure.data_structure_1,
                new_user=mock_user,
                user=mock_owner,
            )

    def test_change_owner_from_anonymous_to_user_raises_exception(self):

        mock_user = create_mock_user("2")
        with self.assertRaises(AccessControlError):
            user_data_structure_api.change_owner(
                document=fixture_data_structure.data_structure_1,
                new_user=mock_user,
                user=AnonymousUser(),
            )

    def test_change_owner_as_superuser_ok(self):
        mock_user = create_mock_user("2", is_superuser=True)
        user_data_structure_api.change_owner(
            document=fixture_data_structure.data_structure_1,
            new_user=mock_user,
            user=mock_user,
        )
