""" Fixtures file for template version manager
"""

from core_main_app.components.template.models import Template
from core_main_app.utils.integration_tests.fixture_interface import (
    FixtureInterface,
)
from core_user_registration_app.components.user_template_version_manager.models import (
    UserTemplateVersionManager,
)


class UserTemplateVersionManagerAccessControlFixtures(FixtureInterface):
    """Template Version Manager fixtures"""

    user1_template = None
    user2_template = None
    global_template = None
    user1_utvm = None
    user2_utvm = None
    global_tvm = None
    template_vm_collection = None

    def insert_data(self):
        """Insert a set of Templates and Template Version Managers.

        Returns:

        """
        # Make a connexion with a mock database
        xsd = (
            '<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">'
            '<xs:element name="tag"></xs:element></xs:schema>'
        )
        self.user1_utvm = UserTemplateVersionManager(
            title="template 1",
            user="1",
            is_disabled=False,
        )
        self.user1_utvm.save()
        self.user1_template = Template(
            filename="template1.xsd",
            content=xsd,
            _hash="hash1",
            user="1",
            version_manager=self.user1_utvm,
            is_current=True,
        )
        self.user1_template.save()
        self.user2_utvm = UserTemplateVersionManager(
            title="template 2",
            user="2",
            is_disabled=False,
        )
        self.user2_utvm.save()
        self.user2_template = Template(
            filename="template2.xsd",
            content=xsd,
            _hash="hash2",
            user="2",
            version_manager=self.user2_utvm,
            is_current=True,
        )
        self.user2_template.save()
        self.global_tvm = UserTemplateVersionManager(
            title="global template",
            user=None,
            is_disabled=False,
        )
        self.global_tvm.save()
        self.global_template = Template(
            filename="global_template.xsd",
            content=xsd,
            _hash="global hash",
            user=None,
            version_manager=self.global_tvm,
            is_current=True,
        )
        self.global_template.save()

        self.template_vm_collection = [
            self.user1_utvm,
            self.user2_utvm,
            self.global_tvm,
        ]
