"""AJAX views
"""

import json

from django.contrib import messages
from django.http.response import HttpResponseBadRequest, HttpResponse

from core_main_app.access_control.exceptions import AccessControlError
from core_main_app.commons.exceptions import DoesNotExist
from core_main_app.utils.xml import validate_xml_data
from core_parser_app.components.data_structure_element import (
    api as data_structure_element_api,
)
from core_parser_app.tools.parser.renderer.xml import XmlRenderer
from core_user_registration_app.components.account_request_metadata import (
    api as account_request_metadata_api,
)
from core_user_registration_app.components.user_data_structure import (
    api as user_data_structure_api,
)
from core_user_registration_app.components.user_metadata import api as data_api
from core_user_registration_app.components.user_metadata.models import (
    UserMetadata,
)
from xml_utils.xsd_tree.xsd_tree import XSDTree


def save_data(request):
    response_dict = {}
    try:

        # get user data structure
        user_data_structure_id = request.POST["id"]
        account_request_metadata_id = request.POST["metadata"]
        user_data_structure = user_data_structure_api.get_by_id(
            user_data_structure_id
        )

        # generate xml data
        xml_data = render_xml(
            user_data_structure.data_structure_element_root, request
        )

        # update user data structure data
        user_data_structure.form_string = xml_data

        # save data structure
        user_data_structure_api.upsert(user_data_structure, request.user)

        # build trees
        xsd_tree = XSDTree.build_tree(user_data_structure.template.content)
        xml_tree = XSDTree.build_tree(xml_data)

        # validate XML document
        errors = validate_xml_data(xsd_tree, xml_tree, request=request)
        if errors is not None:
            response_dict["errors"] = errors

        if errors is None:
            # generate the XML
            xml_data = render_xml(
                user_data_structure.data_structure_element_root, request
            )

            # create new data
            data = UserMetadata()
            data.title = user_data_structure.name
            data.template = user_data_structure.template
            data.user_id = str(request.user.id)
            data.id = user_data_structure.pk

            # set content
            data.xml_content = xml_data
            # save data
            data_api.upsert(data, request.user)
            # insert Metadata reference in account request
            account_request_metadata_api.insert_metadata(
                request.user, account_request_metadata_id, data
            )
            user_data_structure_api.delete(user_data_structure, request.user)
            messages.add_message(
                request, messages.SUCCESS, "User metadata saved."
            )
    except Exception as e:
        message = str(e).replace('"', "'")
        return HttpResponseBadRequest(
            message, content_type="application/javascript"
        )

    return HttpResponse(
        json.dumps({"data_id": str(data.id)}),
        content_type="application/javascript",
    )


def render_xml(root_element, request):
    """Render the XML.

    Args:
        root_element:

    Returns:

    """
    # build XML renderer
    xml_renderer = XmlRenderer(root_element, request)

    # generate xml data
    xml_data = xml_renderer.render()

    return xml_data


def data_structure_element_value(request):
    """Endpoint for data structure element value

    Args:
        request:

    Returns:

    """
    if request.method == "GET":
        return get_data_structure_element_value(request)
    elif request.method == "POST":
        return save_data_structure_element_value(request)


def get_data_structure_element_value(request):
    """Gets the value of a data structure element

    Args:
        request:

    Returns:

    """
    if "id" not in request.GET:
        return HttpResponseBadRequest()

    try:
        element = data_structure_element_api.get_by_id(
            request.GET["id"], request
        )
        element_value = element.value

        if element.tag == "module":
            element_value = {
                "data": element.options["data"],
                "attributes": element.options["attributes"],
            }

        return HttpResponse(
            json.dumps({"value": element_value}),
            content_type="application/json",
        )
    except (AccessControlError, DoesNotExist) as exc:
        return HttpResponseBadRequest(json.dumps({"message": str(exc)}))


def save_data_structure_element_value(request):
    """Saves the value of a data structure element

    Args:
        request:

    Returns:

    """
    if "id" not in request.POST or "value" not in request.POST:
        return HttpResponseBadRequest(
            "Error when trying to data structure element: id or value is missing."
        )

    try:
        input_element = data_structure_element_api.get_by_id(
            request.POST["id"], request
        )

        input_previous_value = input_element.value
        input_element.value = request.POST["value"]
        data_structure_element_api.upsert(input_element, request)

        return HttpResponse(
            json.dumps({"replaced": input_previous_value}),
            content_type="application/json",
        )
    except (AccessControlError, DoesNotExist) as exc:
        return HttpResponseBadRequest(json.dumps({"message": str(exc)}))
