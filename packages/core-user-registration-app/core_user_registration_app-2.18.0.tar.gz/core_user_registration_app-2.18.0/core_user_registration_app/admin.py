""" Url router for the administration site
"""

from django.contrib import admin
from django.urls import re_path

from core_main_app.admin import core_admin_site
from core_main_app.components.template_version_manager.admin_site import (
    CustomTemplateVersionManagerAdmin,
)
from core_main_app.utils.admin_site.view_only_admin import ViewOnlyAdmin
from core_parser_app.components.data_structure.admin_site import (
    CustomDataStructureAdmin,
)
from core_user_registration_app.components.account_request_metadata.models import (
    AccountRequestMetadata,
)
from core_user_registration_app.components.user_data_structure.models import (
    UserDataStructure,
)
from core_user_registration_app.components.user_metadata.models import (
    UserMetadata,
)
from core_user_registration_app.components.user_template_version_manager.models import (
    UserTemplateVersionManager,
)
from core_user_registration_app.views.admin import (
    views as admin_views,
    ajax as admin_ajax,
)

admin_urls = [
    re_path(
        r"^user-template/version/(?P<pk>\w+)/current/$",
        admin_ajax.CurrentTemplateVersion.as_view(),
        name="core_user_registration_app_template_version_current",
    ),
    re_path(
        r"^user-template$",
        admin_views.manage_user_templates,
        name="core_user_registration_app_templates",
    ),
    re_path(
        r"^user-template/versions/(?P<version_manager_id>\w+)",
        admin_views.manage_user_template_versions,
        name="core_user_registration_app_manage_template_versions",
    ),
    re_path(
        r"user-template/upload",
        admin_views.upload_template,
        name="core_user_registration_app_upload_template",
    ),
    # Overrides user-requests
    re_path(
        r"^user-registration-requests$",
        admin_views.user_requests,
        name="core_website_app_user_requests",
    ),
    re_path(
        r"^metadata",
        admin_views.ViewMetaData.as_view(
            administration=True,
            template="core_main_registry_app/admin/data/view_data.html",
        ),
        name="core_user_registration_app_metadata_detail",
    ),
    re_path(
        r"^template/version/current",
        admin_ajax.set_current_template_version_from_version_manager,
        name="core_user_registration_app_set_current_template_version",
    ),
]

admin.site.register(UserDataStructure, CustomDataStructureAdmin)
admin.site.register(AccountRequestMetadata, ViewOnlyAdmin)
admin.site.register(UserMetadata, ViewOnlyAdmin)
admin.site.register(
    UserTemplateVersionManager, CustomTemplateVersionManagerAdmin
)
urls = core_admin_site.get_urls()
core_admin_site.get_urls = lambda: admin_urls + urls
