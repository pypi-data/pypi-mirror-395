from enum import Enum

from django.conf import settings
from django.utils.module_loading import import_string


JOB_NAME_FUNCTION_REGISTRY = import_string(settings.JOB_NAME_FUNCTION_REGISTRY)


class JobStatusEnum(Enum):
    SUCCESS = 'S'
    FAILED = 'F'

    @classmethod
    def to_dict(cls):
        """Returns code -> description mapping for populating reference table"""
        return {status.name: status.value for status in JobStatusEnum}
