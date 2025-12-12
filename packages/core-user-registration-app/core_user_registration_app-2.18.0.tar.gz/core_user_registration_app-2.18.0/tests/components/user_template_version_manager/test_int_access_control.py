""" Access control testing
"""

from tests.components.user_template_version_manager.fixtures.fixtures import (
    UserTemplateVersionManagerAccessControlFixtures,
)

from core_main_app.access_control.exceptions import AccessControlError
from core_main_app.commons.exceptions import CoreError
from core_main_app.utils.integration_tests.integration_base_test_case import (
    IntegrationBaseTestCase,
)
from core_main_app.utils.tests_tools.MockUser import create_mock_user
from core_main_app.utils.tests_tools.RequestMock import create_mock_request
from core_user_registration_app.components.user_template_version_manager import (
    api as user_template_vm_api,
)

fixture_template_vm = UserTemplateVersionManagerAccessControlFixtures()


# FIXME: missing tests where CAN_ANONYMOUS_ACCESS_PUBLIC_DOCUMENT is True


class TestTemplateVersionManagerInsert(IntegrationBaseTestCase):
    """TestTemplateVersionManagerInsert"""

    fixture = fixture_template_vm

    def setUp(self):
        """setUp

        Returns:

        """
        self.anonymous_user = create_mock_user(user_id=None, is_anonymous=True)
        self.user1 = create_mock_user(user_id="1")
        self.staff_user1 = create_mock_user(user_id="1", is_staff=True)
        self.superuser1 = create_mock_user(user_id="1", is_superuser=True)
        self.fixture.insert_data()

    def test_insert_user_template_as_anonymous_raises_access_control_error(
        self,
    ):
        """test_insert_user_template_as_anonymous_raises_access_control_error

        Returns:

        """
        mock_request = create_mock_request(user=self.anonymous_user)
        with self.assertRaises(AccessControlError):
            user_template_vm_api.insert(
                self.fixture.user1_utvm,
                self.fixture.user1_template,
                request=mock_request,
            )

    def test_insert_global_template_as_anonymous_raises_access_control_error(
        self,
    ):
        """test_insert_global_template_as_anonymous_raises_access_control_error

        Returns:

        """
        mock_request = create_mock_request(user=self.anonymous_user)
        with self.assertRaises(AccessControlError):
            user_template_vm_api.insert(
                self.fixture.global_tvm,
                self.fixture.global_template,
                request=mock_request,
            )

    def test_insert_own_template_as_user_saves(self):
        """test_insert_own_template_as_user_saves

        Returns:

        """
        mock_request = create_mock_request(user=self.user1)
        user_template_vm_api.insert(
            self.fixture.user1_utvm,
            self.fixture.user1_template,
            request=mock_request,
        )

    def test_insert_other_users_template_as_user_raises_access_control_error(
        self,
    ):
        """test_insert_other_users_template_as_user_raises_access_control_error

        Returns:

        """
        mock_request = create_mock_request(user=self.user1)
        with self.assertRaises(AccessControlError):
            user_template_vm_api.insert(
                self.fixture.user2_utvm,
                self.fixture.user2_template,
                request=mock_request,
            )

    def test_insert_global_template_as_user_raises_access_control_error(self):
        """test_insert_global_template_as_user_raises_access_control_error

        Returns:

        """
        mock_request = create_mock_request(user=self.user1)
        with self.assertRaises(AccessControlError):
            user_template_vm_api.insert(
                self.fixture.global_tvm,
                self.fixture.global_template,
                request=mock_request,
            )

    def test_insert_own_template_as_staff_saves(self):
        """test_insert_own_template_as_staff_saves

        Returns:

        """
        mock_request = create_mock_request(user=self.staff_user1)
        user_template_vm_api.insert(
            self.fixture.user1_utvm,
            self.fixture.user1_template,
            request=mock_request,
        )

    def test_insert_other_users_template_as_staff_raises_access_control_error(
        self,
    ):
        """test_insert_other_users_template_as_staff_raises_access_control_error

        Returns:

        """
        mock_request = create_mock_request(user=self.staff_user1)
        with self.assertRaises(AccessControlError):
            user_template_vm_api.insert(
                self.fixture.user2_utvm,
                self.fixture.user2_template,
                request=mock_request,
            )

    def test_insert_global_template_as_staff_saves(self):
        """test_insert_global_template_as_staff_saves

        Returns:

        """
        mock_request = create_mock_request(user=self.staff_user1)
        user_template_vm_api.insert(
            self.fixture.global_tvm,
            self.fixture.global_template,
            request=mock_request,
        )

    def test_insert_own_template_as_superuser_saves(self):
        """test_insert_own_template_as_superuser_saves

        Returns:

        """
        mock_request = create_mock_request(user=self.superuser1)
        user_template_vm_api.insert(
            self.fixture.user1_utvm,
            self.fixture.user1_template,
            request=mock_request,
        )

    def test_insert_other_users_template_as_superuser_saves(self):
        """test_insert_other_users_template_as_superuser_saves

        Returns:

        """
        mock_request = create_mock_request(user=self.superuser1)
        user_template_vm_api.insert(
            self.fixture.user2_utvm,
            self.fixture.user2_template,
            request=mock_request,
        )

    def test_insert_global_template_as_superuser_saves(self):
        """test_insert_global_template_as_superuser_saves

        Returns:

        """
        mock_request = create_mock_request(user=self.superuser1)
        user_template_vm_api.insert(
            self.fixture.global_tvm,
            self.fixture.global_template,
            request=mock_request,
        )

    def test_insert_global_template_as_staff_with_wrong_format_raises_core_error(
        self,
    ):
        """test_insert_global_template_as_staff_with_wrong_format_raises_core_error

        Returns:

        """
        mock_request = create_mock_request(user=self.staff_user1)
        self.fixture.global_template.filename = "schema.json"
        with self.assertRaises(CoreError):
            user_template_vm_api.insert(
                self.fixture.global_tvm,
                self.fixture.global_template,
                request=mock_request,
            )


class TestTemplateGetGlobalVersionManagers(IntegrationBaseTestCase):
    """TestTemplateGetGlobalVersionManagers"""

    fixture = fixture_template_vm

    def setUp(self):
        """setUp

        Returns:

        """
        self.anonymous_user = create_mock_user(user_id=None, is_anonymous=True)
        self.user1 = create_mock_user(user_id="1")
        self.staff_user1 = create_mock_user(user_id="1", is_staff=True)
        self.superuser1 = create_mock_user(user_id="1", is_superuser=True)
        self.fixture.insert_data()

    def test_get_global_version_managers_as_anonymous_raises_access_control_error(
        self,
    ):
        """test_get_global_version_managers_as_anonymous_raises_access_control_error

        Returns:

        """
        mock_request = create_mock_request(user=self.anonymous_user)
        with self.assertRaises(AccessControlError):
            user_template_vm_api.get_global_version_managers(
                request=mock_request
            )

    def test_get_global_version_managers_as_user_returns_global_tvm(self):
        """test_get_global_version_managers_as_user_returns_global_tvm

        Returns:

        """
        mock_request = create_mock_request(user=self.user1)
        list_tvm = user_template_vm_api.get_global_version_managers(
            request=mock_request
        )
        for tvm in list_tvm:
            self.assertEqual(tvm.user, None)

    def test_get_global_version_managers_as_staff_returns_global_tvm(self):
        """test_get_global_version_managers_as_staff_returns_global_tvm

        Returns:

        """
        mock_request = create_mock_request(user=self.staff_user1)
        list_tvm = user_template_vm_api.get_global_version_managers(
            request=mock_request
        )
        for tvm in list_tvm:
            self.assertEqual(tvm.user, None)

    def test_get_global_version_managers_as_superuser_returns_global_tvm(self):
        """test_get_global_version_managers_as_superuser_returns_global_tvm

        Returns:

        """
        mock_request = create_mock_request(user=self.superuser1)
        list_tvm = user_template_vm_api.get_global_version_managers(
            request=mock_request
        )
        for tvm in list_tvm:
            self.assertEqual(tvm.user, None)
