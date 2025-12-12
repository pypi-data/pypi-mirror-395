"""
User registration app menu
"""

from django.urls import reverse
from menu import Menu, MenuItem


templates_children = (
    MenuItem(
        "User Template List",
        reverse("core-admin:core_user_registration_app_templates"),
        icon="list",
    ),
    MenuItem(
        "Upload New User Template",
        reverse("core-admin:core_user_registration_app_upload_template"),
        icon="upload",
    ),
)

Menu.add_item(
    "admin", MenuItem("USER TEMPLATES", None, children=templates_children)
)
