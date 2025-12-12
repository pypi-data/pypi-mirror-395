""" AccountRequestMetadata model
"""

from django.db import models

from core_user_registration_app.components.user_metadata.models import (
    UserMetadata,
)
from core_website_app.components.account_request.models import AccountRequest


class AccountRequestMetadata(AccountRequest):
    """AccountRequestMetadata."""

    metadata = models.ForeignKey(
        UserMetadata, blank=True, on_delete=models.CASCADE, null=True
    )

    class Meta:
        verbose_name = "Account request metadata"
        verbose_name_plural = "Account request metadata"

    @staticmethod
    def get_all():
        """Get all Account Request Metadata

        Returns:

        """
        return AccountRequestMetadata.objects.all()
