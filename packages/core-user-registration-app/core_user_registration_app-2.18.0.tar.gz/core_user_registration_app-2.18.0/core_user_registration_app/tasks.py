"""User Registration tasks """

import logging

from celery import shared_task

from core_main_app.utils.datetime import datetime_now, datetime_timedelta
from core_user_registration_app.components.user_data_structure.models import (
    UserDataStructure,
)
from core_user_registration_app.settings import (
    USER_DATA_STRUCTURE_HOURS_THRESHOLD,
)
from core_user_registration_app.system import api as system_api

logger = logging.getLogger(__name__)


@shared_task
def delete_user_data_structure():
    """DELETES every DELETE_USER_DATA_STRUCTURE_RATE the UserDataStructure in the DataStructure collection"""
    logger.info("Checking Old UserDataStructures")
    try:
        user_data_structure_perm = UserDataStructure.get_permission()
        for (
            data_structure_element
        ) in system_api.get_all_data_structure_elements():
            if (
                data_structure_element.data_structure
                and data_structure_element.data_structure.get_object_permission()
                == user_data_structure_perm
            ):
                if (
                    data_structure_element.creation_date
                    < datetime_now()
                    - datetime_timedelta(
                        hours=USER_DATA_STRUCTURE_HOURS_THRESHOLD
                    )
                ):
                    data_structure_element.delete()
        logger.info("FINISH checking DataStructures.")

    except Exception as e:
        logger.error(f"ERROR : Error while deleting data structures: {str(e)}")
