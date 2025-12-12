"""
Template Version Manager model
"""

from django.core.exceptions import ObjectDoesNotExist
from django.db import models

from core_main_app.commons import exceptions
from core_main_app.components.template_version_manager.models import (
    TemplateVersionManager,
)


class UserTemplateVersionManager(TemplateVersionManager):
    """Manager of templates versions"""

    # TODO: see if better way to find _cls
    _class_name = "VersionManager.UserTemplateVersionManager"
    is_default = models.BooleanField(default=False)

    @property
    def class_name(self):
        return UserTemplateVersionManager._class_name

    @staticmethod
    def get_by_id(version_manager_id):
        """Return Version Managers by id.

        Args:
            version_manager_id:

        Returns:

        """
        try:
            return UserTemplateVersionManager.objects.get(
                pk=version_manager_id
            )
        except ObjectDoesNotExist as e:
            raise exceptions.DoesNotExist(str(e))
        except Exception as e:
            raise exceptions.ModelError(str(e))

    @staticmethod
    def get_global_version_managers(_cls=True):
        """Return all Template Version Managers with user set to None.

        Returns:
            _cls: if True, restricts to TemplateVersionManager _cls
        """
        queryset = UserTemplateVersionManager.objects.filter(user=None).all()
        if _cls:
            queryset = queryset.filter(
                _cls=UserTemplateVersionManager._class_name
            ).all()
        return queryset

    def save_template_version_manager(self):
        """Custom save.

        Returns:
            Saved Instance.

        """
        return super(UserTemplateVersionManager, self).save_version_manager()

    @staticmethod
    def get_default_version_manager():
        """Return default User Version Manager.

        Returns:

        """
        return UserTemplateVersionManager.objects(is_default=True)

    @staticmethod
    def get_active_global_version_manager_by_title(version_manager_title):
        """Return active Template Version Manager by its title with user set to None.

        Args:
            version_manager_title: Version Manager title

        Returns:
            Version Manager instance

        """
        try:
            return UserTemplateVersionManager.objects.get(
                is_disabled=False, title=version_manager_title, user=None
            )
        except ObjectDoesNotExist as e:
            raise exceptions.DoesNotExist(str(e))
        except Exception as e:
            raise exceptions.ModelError(str(e))
