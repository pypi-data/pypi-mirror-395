from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.shortcuts import redirect
from django.template.loader import get_template
from django.urls import reverse
from django.views import View

from core_curate_app.views.user.views import generate_form, render_form
from core_main_app.commons.exceptions import ApiError
from core_main_app.utils.rendering import render
from core_user_registration_app.components.account_request_metadata import (
    api as account_request_metadata_api,
)
from core_user_registration_app.components.user_data_structure import (
    api as user_data_structure_api,
)
from core_user_registration_app.components.user_data_structure.models import (
    UserDataStructure,
)
from core_user_registration_app.components.user_template_version_manager import (
    api as user_version_manager_api,
)
from core_website_app.views.user.forms import RequestAccountForm


def request_new_account(request):
    assets = {
        "js": [
            {
                "path": "core_website_app/user/js/user_account_req.js",
                "is_raw": False,
            }
        ],
        "css": ["core_website_app/user/css/list.css"],
    }

    if request.method == "POST":
        request_form = RequestAccountForm(request.POST)
        if request_form.is_valid():
            # Call the API
            try:
                request_form_data = request_form.cleaned_data
                version_manager = (
                    user_version_manager_api.get_default_version_manager()
                )

                template = version_manager[0].current_version
                name = request.POST["username"]

                user = User(
                    username=request_form_data.get("username"),
                    first_name=request_form_data.get("firstname"),
                    last_name=request_form_data.get("lastname"),
                    password=make_password(request_form_data.get("password1")),
                    email=request_form_data.get("email"),
                    is_active=False,
                )

                user_data_structure = UserDataStructure(
                    user=name, template=template, name=name
                )

                user_data_structure_api.upsert(user_data_structure, user)
                objectid = user_data_structure.id

                account_request = (
                    account_request_metadata_api.create_account_request(user)
                )
                messages.add_message(
                    request,
                    messages.INFO,
                    "User Account Request sent to the administrator.",
                )

                url = reverse(
                    "core_user_registration_app_account_metadata",
                    args=(objectid, account_request.id),
                )
                return redirect(url)

            except ApiError as e:
                error_message = str(e)

                error_template = get_template(
                    "core_website_app/user/request_error.html"
                )
                error_box = error_template.render(
                    {"error_message": error_message}
                )

                return render(
                    request,
                    "core_website_app/user/request_new_account.html",
                    assets=assets,
                    context={
                        "request_form": request_form,
                        "action_result": error_box,
                        "page_title": "Error",
                    },
                )
            except ValidationError as e:
                error_message = (
                    "The following error(s) occurred during " "validation:"
                )
                error_items = [str(error) for error in e.messages]

                error_template = get_template(
                    "core_website_app/user/request_error.html"
                )
                error_box = error_template.render(
                    {
                        "error_message": error_message,
                        "error_items": error_items,
                    }
                )

                return render(
                    request,
                    "core_website_app/user/request_new_account.html",
                    assets=assets,
                    context={
                        "request_form": request_form,
                        "action_result": error_box,
                        "page_title": "Error",
                    },
                )

    else:
        request_form = RequestAccountForm()

    context = {"request_form": request_form}
    # Set page title
    context.update({"page_title": "Account Request"})

    return render(
        request,
        "core_user_registration_app/user/request_new_account.html",
        assets=assets,
        context=context,
    )


class AccountCreationView(View):
    def __init__(self):
        super(AccountCreationView, self).__init__()
        self.assets = {
            "js": [
                {
                    "path": "core_user_registration_app/user/js/save_data.js",
                    "is_raw": False,
                },
                {
                    "path": "core_user_registration_app/user/js/save_data.raw.js",
                    "is_raw": False,
                },
                {
                    "path": "core_parser_app/js/autosave.js",
                    "is_raw": False,
                },
                {
                    "path": "core_user_registration_app/user/js/autosave.raw.js",
                    "is_raw": True,
                },
                {
                    "path": "core_user_registration_app/user/js/report_data.js",
                    "is_raw": False,
                },
                {
                    "path": "core_user_registration_app/user/js/report_data.raw.js",
                    "is_raw": True,
                },
            ],
            "css": ["core_curate_app/user/css/xsd_form.css"],
        }

    def get(self, request, objectid, accountid):
        context = self.build_context(request, objectid, accountid)
        # Set page title
        context.update({"page_title": "Account Creation"})
        return render(
            request,
            "core_user_registration_app/user/account_creation.html",
            assets=self.assets,
            context=context,
        )

    def build_context(self, request, objectid, account_id):
        """Builds the context.

        Args:
            request:
            objectid:

        Returns:

        """
        #
        user_data_structure = user_data_structure_api.get_by_id(objectid)
        xsd_string = user_data_structure.template.content
        xml_string = user_data_structure.form_string
        root_element = generate_form(
            xsd_string, xml_string, user_data_structure, request
        )
        user_data_structure_api.update_data_structure_root(
            user_data_structure, root_element, request.user
        )
        xsd_form = render_form(request, root_element)

        return {
            "edit": True if user_data_structure.data is not None else False,
            "xsd_form": xsd_form,
            "data_structure": user_data_structure,
            "account_id": account_id,
        }
