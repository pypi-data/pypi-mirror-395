""" Fixtures files for UserMetadata
"""

from core_main_app.components.template.models import Template
from core_main_app.components.workspace.models import Workspace
from core_main_app.utils.integration_tests.fixture_interface import (
    FixtureInterface,
)
from core_user_registration_app.components.user_metadata.models import (
    UserMetadata,
)


class DataFixtures(FixtureInterface):
    """UserMetadata fixtures"""

    data_1 = None
    data_2 = None
    data_3 = None
    template = None
    data_collection = None

    def insert_data(self):
        """Insert a set of UserMetadata.

        Returns:

        """
        # Make a connexion with a mock database
        self.generate_template()
        self.generate_data_collection()

    def generate_data_collection(self):
        """Generate a UserMetadata collection.

        Returns:

        """
        # NOTE: no xml_content to avoid using unsupported GridFS mock
        self.data_1 = UserMetadata(
            template=self.template,
            user_id="1",
            dict_content=None,
            title="title",
        )
        self.data_1.save()
        self.data_2 = UserMetadata(
            template=self.template,
            user_id="2",
            dict_content=None,
            title="title2",
        )
        self.data_2.save()
        self.data_3 = UserMetadata(
            template=self.template,
            user_id="1",
            dict_content=None,
            title="title3",
        )
        self.data_3.save()
        self.data_collection = [self.data_1, self.data_2, self.data_3]

    def generate_template(self):
        """Generate an unique Template.

        Returns:

        """
        self.template = Template()
        xsd = (
            '<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">'
            '<xs:element name="tag"></xs:element></xs:schema>'
        )
        self.template.content = xsd
        self.template.hash = ""
        self.template.filename = "filename.xsd"
        self.template.save()


class AccessControlDataFixture(FixtureInterface):
    """Access Control UserMetadata fixture"""

    USER_1_NO_WORKSPACE = 0
    USER_2_NO_WORKSPACE = 1
    USER_1_WORKSPACE_1 = 2
    USER_2_WORKSPACE_2 = 3

    template = None
    workspace_1 = None
    workspace_2 = None
    data_collection = None
    data_1 = None
    data_2 = None
    data_3 = None
    data_4 = None
    data_5 = None

    def insert_data(self):
        """Insert a set of UserMetadata.

        Returns:

        """
        # Make a connexion with a mock database
        self.generate_template()
        self.generate_workspace()
        self.generate_data_collection()

    def generate_data_collection(self):
        """Generate a UserMetadata collection.

        Returns:

        """

        content = {"root": {"element": "value2"}}

        self.data_1 = UserMetadata(
            template=self.template, title="Data 1", user_id="1"
        )
        self.data_1.save()
        self.data_2 = UserMetadata(
            template=self.template, title="Data 2", user_id="2"
        )
        self.data_2.save()
        self.data_3 = UserMetadata(
            template=self.template,
            title="Data 3",
            user_id="1",
            workspace=self.workspace_1,
            dict_content=content,
        )
        self.data_3.save()
        self.data_4 = UserMetadata(
            template=self.template,
            title="DataDoubleTitle",
            user_id="2",
            workspace=self.workspace_2,
        )
        self.data_4.save()
        self.data_5 = UserMetadata(
            template=self.template,
            title="DataDoubleTitle",
            user_id="1",
            workspace=self.workspace_1,
        )
        self.data_5.save()

        self.data_collection = [
            self.data_1,
            self.data_2,
            self.data_3,
            self.data_4,
            self.data_5,
        ]

    def generate_template(self):
        """Generate an unique Template.

        Returns:

        """
        self.template = Template()
        xsd = (
            '<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">'
            '<xs:element name="tag"></xs:element></xs:schema>'
        )
        self.template.content = xsd
        self.template.hash = ""
        self.template.filename = "filename.xsd"
        self.template.save()

    def generate_workspace(self):
        """Generate the workspaces.

        Returns:

        """
        self.workspace_1 = Workspace(
            title="Workspace 1", owner="1", read_perm_id="1", write_perm_id="1"
        )
        self.workspace_1.save()
        self.workspace_2 = Workspace(
            title="Workspace 2", owner="2", read_perm_id="2", write_perm_id="2"
        )
        self.workspace_2.save()
