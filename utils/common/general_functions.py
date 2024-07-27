# webapp/features/general_functions.py
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist

import logging

logger = logging.getLogger(__name__)
User = get_user_model()

# Default User id for instance created by value : user -2 : anandvm
common_user_id = '433714f1-0f09-4363-a51c-9d99a29d88a6'


def err_msg(obj):
    try:
        error_messages = {}
        if isinstance(obj, dict):  # Check if it's a DRF Serializer error.
            for field, errors in obj.items():
                error_messages[field] = errors[0] if isinstance(errors, list) else errors

        elif hasattr(obj, 'get_codes'):  # Check if it's a DRF ValidationError
            for field, errors in obj.get_codes().items():
                error_messages[field] = obj.get_full_details()[field][0]['message']
        else:
            error_messages = str(obj)
        return error_messages
    except Exception as ex:
        logger.error(ex)
        return "Unknown Error"




    def get_error_messages(self, obj):
        error_messages = {}
        if isinstance(obj, dict):  # Check if it's a DRF Serializer error.
            for field, errors in obj.items():
                error_messages[field] = errors[0] if isinstance(errors, list) else errors

        if hasattr(obj, 'get_codes'):  # Check if it's a DRF ValidationError
            for field, errors in obj.get_codes().items():
                error_messages[field] = obj.get_full_details()[field][0]['message']
        return error_messages

def get_user_from_uuid(uuid_string):
    try:
        user = User.objects.get(uuid=str(uuid_string))
        return user
    except ObjectDoesNotExist:
        logger.info(f"User not found with UUID : {uuid_string}")
        return None
    except Exception as e:
        logger.error(f" Something went wrong :{e}")
        return None


def create_notification_by_model(user_uuid, title, message):
    try:
        content_type = ContentType.objects.get(app_label='user', model='Notifications')
        model_class = content_type.model_class()
        user = get_user_from_uuid(user_uuid)
        if model_class:
            notification_object = model_class.objects.create(
                user=user,
                title=title,
                message=message,
                created_by=str(user_uuid),
                created_at=timezone.now()
            )
            return notification_object
    except ContentType.DoesNotExist:
        logger.error(f" Model object not found")
        return None
    except Exception as e:
        logger.error(f" Something went wrong :{e}")
        return None



