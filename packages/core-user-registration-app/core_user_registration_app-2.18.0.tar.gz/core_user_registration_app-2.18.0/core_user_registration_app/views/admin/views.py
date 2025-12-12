"""
    Admin views
"""

from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.http.response import HttpResponseRedirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.html import escape as html_escape

import core_user_registration_app.components.account_request_metadata.api as account_request_api
from core_main_app.commons import exceptions
from core_main_app.components.template.models import Template
from core_main_app.components.template_version_manager import (
    api as template_version_manager_api,
)
from core_main_app.components.version_manager import api as version_manager_api
from core_main_app.settings import INSTALLED_APPS
from core_main_app.utils.labels import get_data_label
from core_main_app.utils.rendering import admin_render
from core_main_app.views.admin.forms import (
    UploadTemplateForm,
    UploadVersionForm,
)
from core_main_app.views.admin.views import handle_xsd_errors
from core_main_app.views.common.ajax import (
    EditTemplateVersionManagerView,
)
from core_main_app.views.common.views import CommonView
from core_main_app.views.common.views import read_xsd_file
from core_main_app.views.user.views import get_context_manage_template_versions
from core_user_registration_app.components.user_metadata import (
    api as metadata_api,
)
from core_user_registration_app.components.user_template_version_manager import (
    api as user_version_manager_api,
)
from core_user_registration_app.components.user_template_version_manager.models import (
    UserTemplateVersionManager,
)


@staff_member_required
def user_requests(request):
    """Page that allows to accept or deny user requests

    Args:
        request:

    Returns:
    """
    # Call the API
    user = request.user
    requests = account_request_api.get_all(user)

    assets = {
        "js": [
            {
                "path": "core_website_app/admin/js/user_requests.js",
                "is_raw": False,
            },
            {
                "path": "core_user_registration_app/admin/js/view_meta.js",
                "is_raw": False,
            },
            {
                "path": "core_user_registration_app/admin/js/view_meta.raw.js",
                "is_raw": True,
            },
        ],
    }

    modals = [
        "core_website_app/admin/account_requests/modals/deny_request.html",
    ]

    return admin_render(
        request,
        "core_user_registration_app/admin/user_requests.html",
        assets=assets,
        modals=modals,
        context={"requests": requests},
    )


class ViewMetaData(CommonView):
    """
    View detail data.
    """

    template = "core_main_app/user/data/detail.html"

    @method_decorator(staff_member_required)
    def get(self, request, *args, **kwargs):
        data_id = request.GET["id"]
        try:
            data = metadata_api.get_by_id(data_id, request.user)

            context = {"data": data}

            assets = {
                "js": [
                    {
                        "path": "core_main_app/common/js/XMLTree.js",
                        "is_raw": False,
                    },
                    {
                        "path": "core_main_app/user/js/data/detail.js",
                        "is_raw": False,
                    },
                ],
                "css": ["core_main_app/common/css/XMLTree.css"],
            }

            modals = []

            if "core_file_preview_app" in INSTALLED_APPS:
                assets["js"].extend(
                    [
                        {
                            "path": "core_file_preview_app/user/js/file_preview.js",
                            "is_raw": False,
                        }
                    ]
                )
                assets["css"].append(
                    "core_file_preview_app/user/css/file_preview.css"
                )
                modals.append(
                    "core_file_preview_app/user/file_preview_modal.html"
                )
            # Set page title
            context.update({"page_title": "View Metadata"})

            return self.common_render(
                request,
                self.template,
                context=context,
                assets=assets,
                modals=modals,
            )
        except exceptions.DoesNotExist:
            error_message = "Data not found"
        except exceptions.ModelError:
            error_message = "Model error"
        except Exception as e:
            error_message = str(e)

        return self.common_render(
            request,
            "core_main_app/common/commons/error.html",
            context={
                "error": "Unable to access the requested "
                + get_data_label()
                + ": {}.".format(error_message),
                "page_title": "Error",
            },
        )


@staff_member_required
def manage_user_templates(request):
    """View that allows user template management.

    Args:
        request:

    Returns:

    """
    templates = user_version_manager_api.get_global_version_managers(
        request=request
    )
    context = {
        "object_name": "Template",
        "available": [
            template for template in templates if not template.is_disabled
        ],
        "disabled": [
            template for template in templates if template.is_disabled
        ],
        "come_from_user": "True",
    }

    assets = {
        "js": [
            {
                "path": "core_main_app/common/js/templates/list/restore_user.js",
                "is_raw": False,
            },
            {
                "path": "core_main_app/common/js/templates/list/modals/disable_user.js",
                "is_raw": False,
            },
            {
                "path": "core_user_registration_app/common/js/templates/set_current.js",
                "is_raw": False,
            },
            EditTemplateVersionManagerView.get_modal_js_path(),
        ]
    }

    modals = [
        "core_main_app/admin/templates/list/modals/disable.html",
        EditTemplateVersionManagerView.get_modal_html_path(),
    ]

    return admin_render(
        request,
        "core_user_registration_app/admin/templates/list.html",
        assets=assets,
        context=context,
        modals=modals,
    )


@staff_member_required
def manage_user_template_versions(request, version_manager_id):
    """View that allows template versions management.

    Args:
        request:
        version_manager_id:

    Returns:

    """
    try:
        # get the version manager

        version_manager = user_version_manager_api.get_version_manager_by_id(
            version_manager_id
        )
        context = get_context_manage_template_versions(version_manager)
        if "core_parser_app" in settings.INSTALLED_APPS:
            context.update(
                {"module_url": "admin:core_parser_app_template_modules"}
            )

        assets = {
            "js": [
                {
                    "path": "core_user_registration_app/common/js/templates/versions/set_current.js",
                    "is_raw": False,
                },
                {
                    "path": "core_user_registration_app/common/js/templates/versions/set_current.raw.js",
                    "is_raw": True,
                },
                {
                    "path": "core_main_app/common/js/templates/versions/restore.js",
                    "is_raw": False,
                },
                {
                    "path": "core_main_app/common/js/templates/versions/modals/disable.js",
                    "is_raw": False,
                },
            ]
        }

        modals = ["core_main_app/admin/templates/versions/modals/disable.html"]

        return admin_render(
            request,
            "core_user_registration_app/admin/templates/versions.html",
            assets=assets,
            modals=modals,
            context=context,
        )
    except Exception as e:
        return admin_render(
            request,
            "core_main_app/common/commons/error.html",
            context={"error": str(e)},
        )


@staff_member_required
def upload_template(request):
    """Upload template.

    Args:
        request:

    Returns:

    """
    assets = {
        "js": [
            {
                "path": "core_main_app/admin/js/templates/upload/dependency_resolver.js",
                "is_raw": True,
            },
            {
                "path": "core_main_app/admin/js/templates/upload/dependencies.js",
                "is_raw": False,
            },
            {
                "path": "core_main_app/common/js/backtoprevious.js",
                "is_raw": True,
            },
        ]
    }

    context = {
        "object_name": "Template",
        "url": reverse(
            "core-admin:core_user_registration_app_upload_template"
        ),
        "redirect_url": reverse(
            "core-admin:core_user_registration_app_templates"
        ),
    }

    # method is POST
    if request.method == "POST":
        form = UploadTemplateForm(request.POST, request.FILES)
        context["upload_form"] = form

        if form.is_valid():
            return _save_template(request, assets, context)
        else:
            # Display error from the form
            return _upload_template_response(request, assets, context)
    # method is GET
    else:
        # render the form to upload a template
        context["upload_form"] = UploadTemplateForm()
        return _upload_template_response(request, assets, context)


@staff_member_required
def upload_template_version(request, version_manager_id):
    """Upload template version.

    Args:
        request:
        version_manager_id:

    Returns:

    """
    assets = {
        "js": [
            {
                "path": "core_main_app/admin/js/templates/upload/dependency_resolver.js",
                "is_raw": True,
            },
            {
                "path": "core_main_app/admin/js/templates/upload/dependencies.js",
                "is_raw": False,
            },
        ]
    }

    template_version_manager = version_manager_api.get(
        version_manager_id, request=request
    )
    context = {
        "object_name": "Template",
        "version_manager": template_version_manager,
        "url": reverse(
            "admin:core_main_app_upload_template_version",
            kwargs={"version_manager_id": template_version_manager.id},
        ),
        "redirect_url": reverse(
            "admin:core_main_app_manage_template_versions",
            kwargs={"version_manager_id": template_version_manager.id},
        ),
    }

    # method is POST
    if request.method == "POST":
        form = UploadVersionForm(request.POST, request.FILES)
        context["upload_form"] = form

        if form.is_valid():
            return _save_template_version(
                request, assets, context, template_version_manager
            )
        else:
            # Display errors from the form
            return _upload_template_response(request, assets, context)
    # method is GET
    else:
        # render the form to upload a template
        context["upload_form"] = UploadVersionForm()
        return _upload_template_response(request, assets, context)


@staff_member_required
def _save_template(request, assets, context):
    """Save a template.

    Args:
        request:
        assets:
        context:

    Returns:

    """
    # get the schema name
    name = request.POST["name"]
    # get the file from the form
    xsd_file = request.FILES["upload_file"]
    # read the content of the file
    xsd_data = read_xsd_file(xsd_file)
    try:
        template = Template(filename=xsd_file.name, content=xsd_data)
        template_version_manager = UserTemplateVersionManager(title=name)
        user_version_manager_api.insert(
            template_version_manager, template, request=request
        )
        return HttpResponseRedirect(
            reverse("core-admin:core_user_registration_app_templates")
        )
    except exceptions.XSDError as xsd_error:
        return handle_xsd_errors(
            request, assets, context, xsd_error, xsd_data, xsd_file.name
        )
    except exceptions.NotUniqueError:
        context["errors"] = html_escape(
            "A template with the same name already exists. Please choose another name."
        )
        return _upload_template_response(request, assets, context)
    except Exception as e:
        context["errors"] = html_escape(str(e))
        return _upload_template_response(request, assets, context)


@staff_member_required
def _save_template_version(request, assets, context, template_version_manager):
    """Save a template version.

    Args:
        request:
        assets:
        context:
        template_version_manager:

    Returns:

    """
    # get the file from the form
    xsd_file = request.FILES["xsd_file"]
    # read the content of the file
    xsd_data = read_xsd_file(xsd_file)

    try:
        template = Template(filename=xsd_file.name, content=xsd_data)
        template_version_manager_api.insert(
            template_version_manager, template, request=request
        )

        # create the fragment url with all the version of the template (minus the new template)
        version_manager_string = ""
        for version in template_version_manager.versions:
            if version != str(template.id):
                current_version_string = (
                    version if version_manager_string == "" else f",{version}"
                )

                version_manager_string += current_version_string

        # add the fragment data to the url
        fragment = f"#from={version_manager_string}&to={template.id}"

        return HttpResponseRedirect(
            reverse("admin:core_main_app_data_migration") + fragment
        )
    except exceptions.XSDError as xsd_error:
        return handle_xsd_errors(
            request, assets, context, xsd_error, xsd_data, xsd_file.name
        )
    except Exception as e:
        context["errors"] = html_escape(str(e))
        return _upload_template_response(request, assets, context)


@staff_member_required
def _upload_template_response(request, assets, context):
    """Render template upload response.

    Args:
        request:
        context:

    Returns:

    """
    return admin_render(
        request,
        "core_main_app/admin/templates/upload.html",
        assets=assets,
        context=context,
    )
