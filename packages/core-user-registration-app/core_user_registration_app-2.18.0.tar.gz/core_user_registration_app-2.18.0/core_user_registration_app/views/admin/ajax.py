""" REST views for the registry template version manager API
"""

from django.contrib.admin.views.decorators import staff_member_required
from django.http.response import HttpResponseBadRequest, HttpResponse
from rest_framework.permissions import IsAuthenticated

from core_main_app.components.version_manager import api as version_manager_api
from core_main_app.rest.template_version_manager.abstract_views import (
    AbstractStatusTemplateVersion,
)
from core_user_registration_app.components.user_template_version_manager import (
    api as user_version_manager_api,
)


# ACL is done in the AbstractStatusTemplateVersion object
class CurrentTemplateVersion(AbstractStatusTemplateVersion):
    """Update status to current"""

    permission_classes = (IsAuthenticated,)

    def status_update(self, template_object):
        """Update status to current

        Args:

            template_object: template_version

        Returns:

            TemplateVersion
        """
        return version_manager_api.set_current(
            template_object, request=self.request
        )


@staff_member_required
def set_current_template_version_from_version_manager(request):
    """Set the current version of a template.

    Args:
        request:

    Returns:

    """
    try:

        user_version_manager_api.set_default_version_manager(
            request.GET["id"], request
        )
    except Exception as e:
        return HttpResponseBadRequest(
            str(e), content_type="application/javascript"
        )

    return HttpResponse(content_type="application/javascript")
