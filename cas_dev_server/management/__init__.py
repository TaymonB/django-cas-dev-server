import base64
import hashlib
import os

from django.conf import settings
from django.utils.encoding import force_bytes
import environ

def subprocess_environment():
    return dict(os.environ, DJANGO_SETTINGS_MODULE='cas_dev_server.internal.settings',
                SECRET_KEY=base64.b64encode(hashlib.sha256(force_bytes(settings.SECRET_KEY)).digest()),
                DEBUG=str(settings.DEBUG), TEMPLATE_DEBUG=str(settings.TEMPLATE_DEBUG),
                DATABASE_URL=settings.CAS_DEV_DATABASE_URL, LANGUAGE_CODE=settings.LANGUAGE_CODE,
                TIME_ZONE=settings.TIME_ZONE, USE_I18N=str(settings.USE_I18N), USE_L10N=str(settings.USE_L10N),
                USE_TZ=str(settings.USE_TZ))
