from pathlib import Path
import logging

from django.apps import AppConfig
from django.conf import settings

try:
    # Python 3.8+
    from importlib.metadata import version, PackageNotFoundError
except ImportError:
    # Python < 3.8
    from importlib_metadata import version, PackageNotFoundError

logger = logging.getLogger(__name__)


class BackupUtilsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'django_backup_utils'

    PROJECT_NAME = Path(settings.BASE_DIR).name
    JSON_FILENAME = 'django-backup-utils-fullbackup.json'
    DUMPINFO = 'django-backup-utils-backup-info.txt'

    try:
        DJANGO_BACKUP_UTILS_VERSION = version('django-backup-utils')
    except PackageNotFoundError:
        DJANGO_BACKUP_UTILS_VERSION = "unknown"

    try:
        BACKUP_IGNORE_CONSISTENCY = settings.BACKUP_IGNORE_CONSISTENCY
    except AttributeError:
        BACKUP_IGNORE_CONSISTENCY = False

    try:
        BACKUP_DIRS = settings.BACKUP_DIRS
    except AttributeError:
        BACKUP_DIRS = []

    if BACKUP_DIRS:
        # check for dirs
        for directory in BACKUP_DIRS:
            if not Path(directory).is_dir():
                logger.warning(f"The configured BACKUP_DIR {Path(directory)} does not exist.")
