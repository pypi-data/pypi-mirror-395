""" Unit Test for Migrations
"""

from unittest.mock import patch

from django.db.migrations.exceptions import BadMigrationError
from django.test import TestCase

from core_main_app.commons.exceptions import DoesNotExist
from core_user_registration_app import discover
from core_user_registration_app.components.user_template_version_manager.models import (
    UserTemplateVersionManager,
)
from core_user_registration_app.discover import _get_or_create_xslt


class TestInitData(TestCase):
    """TestInitData"""

    @patch.object(UserTemplateVersionManager, "objects")
    def test_migration_stops_when_user_template_manager_already_present(
        self,
        mock_user_tvm_objects,
    ):
        """test_migration_stops_when_user_template_manager_already_present"""
        mock_user_tvm_objects.count.return_value = 1
        discover.init_registration_app()

    @patch("core_user_registration_app.discover.user_registration_settings")
    @patch.object(UserTemplateVersionManager, "objects")
    def test_migration_raises_error_if_setting_not_set(
        self, mock_user_tvm_objects, mock_settings
    ):
        """test_migration_stops_when_user_template_manager_already_present"""
        mock_user_tvm_objects.count.return_value = 0
        mock_settings.REGISTRY_XSD_USER_FILEPATH = None

        with self.assertRaises(BadMigrationError):
            discover.init_registration_app()

    @patch("core_user_registration_app.discover.user_registration_settings")
    @patch.object(UserTemplateVersionManager, "objects")
    def test_migration_raises_error_if_file_does_not_exist(
        self, mock_user_tvm_objects, mock_settings
    ):
        """test_migration_raises_error_if_file_does_not_exist"""
        mock_user_tvm_objects.count.return_value = 0
        mock_settings.REGISTRY_XSD_USER_FILEPATH = "bad"

        with self.assertRaises(BadMigrationError):
            discover.init_registration_app()


class TestGetOrCreateXSLT(TestCase):
    """TestGetOrCreateXSLT"""

    @patch("core_main_app.components.xsl_transformation.api.upsert")
    @patch("core_main_app.utils.file.read_file_content")
    @patch("core_main_app.components.xsl_transformation.api.get_by_name")
    def test_get_or_create_xslt_creates_xslt_if_does_not_exist(
        self,
        mock_xsl_get_by_name,
        mock_read_file_content,
        mock_xsl_upsert,
    ):
        """test_get_or_create_xslt_creates_xslt_if_does_not_exist"""
        mock_xsl_get_by_name.side_effect = DoesNotExist("error")
        mock_read_file_content.return_value = ""
        mock_xsl_upsert.return_value = None

        _get_or_create_xslt(file_path="path", filename="test.xsl")

        self.assertTrue(mock_xsl_upsert.called)
