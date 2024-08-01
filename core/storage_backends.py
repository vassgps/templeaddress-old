# webapp/core/storage_backends.py
from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage
from django.contrib.auth import get_user_model


class StaticStorage(S3Boto3Storage):
    location = settings.AWS_STATIC_LOCATION
    # location = 'static'
    default_acl = 'public-read'


class PublicMediaStorage(S3Boto3Storage):
    location = settings.PUBLIC_MEDIA_LOCATION
    default_acl = 'public-read'
    file_overwrite = False


class PrivateMediaStorage(S3Boto3Storage):
    location = settings.AWS_PRIVATE_MEDIA_LOCATION
    default_acl = 'private'
    file_overwrite = False
    custom_domain = False

    def _get_access_keys(self, name):
        authenticated = False
        user = get_user_model()

        # Check if user is authenticated
        if user.is_authenticated:
            authenticated = True

        if authenticated:
            # Logic to grant access to authenticated users
            return {'AWS_S3_OBJECT_PARAMETERS': {'ACL': 'private'}}
        else:
            # Deny access to unauthenticated users
            return {'AWS_S3_OBJECT_PARAMETERS': {'ACL': 'no-access'}}