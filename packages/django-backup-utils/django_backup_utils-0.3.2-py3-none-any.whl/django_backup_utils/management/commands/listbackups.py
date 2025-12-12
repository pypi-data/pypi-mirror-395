import logging
import os
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.utils.dateparse import parse_datetime

from django_backup_utils.apps import BackupUtilsConfig
from django_backup_utils.helpers import get_backup_name, extract_dumpinfo, get_system_migrations, \
    get_backup_list_by_time

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    def find_backup(self, hostname=None, projectname=None, all=False):
        logger.debug(f"find_backup(hostname={hostname}, projectname={projectname}, all={all})")
        files = os.listdir(settings.BACKUP_ROOT)
        paths = [os.path.join(settings.BACKUP_ROOT, basename) for basename in files]
        correct = []
        logger.debug(f"files in backupdir: {paths}")
        if paths:
            paths.reverse()
            for each in paths:
                file = get_backup_name(each, hostname, projectname, all)
                if file:
                    correct.append(each)
        else:
            print(f"no backups found")
        return correct

    def add_arguments(self, parser):
        parser.add_argument('--hostname', type=str, help="show backups for specified hostname")
        parser.add_argument('--projectname', type=str, help="show backups for specified django project")
        parser.add_argument('--all', action='store_true', help="show all backups")
        parser.add_argument('--showinfo', action='store_true', help="show backup metadata")
        parser.add_argument('--showlatest', action='store_true', help="show only latest backup")

    def handle(self, hostname, projectname, all, showinfo, showlatest, *args, **options):
        if os.path.exists(settings.BACKUP_ROOT):

            sorted_backups = get_backup_list_by_time(settings.BACKUP_ROOT, hostname, projectname, all)

            if not sorted_backups:
                print("no backups found")
            else:
                if showinfo:
                    system_migrations_migrated, system_migrations_files = get_system_migrations()

                if showlatest:
                    sorted_backups = [sorted_backups[-1]]

                for index, backup in enumerate(sorted_backups):
                    prefix = f"{index + 1}\t  "
                    if index == len(sorted_backups) - 1:
                        prefix = f"{index + 1} (latest)"
                    print(prefix, f"\t\t\t{backup.get('path')}")
                    if showinfo:
                        info = extract_dumpinfo(Path(backup.get('path')))
                        time = parse_datetime(info.get('created_at'))
                        print(f"created at:\t\t\t{time.astimezone(tz=timezone.get_current_timezone())}")
                        print(
                            f"size:\t\t\t\t{round(float(Path(backup.get('path')).stat().st_size / 1000 / 1000), 4)} MB")
                        print(f"backup directories: \t\t{info.get('backup_directories')}\n")
                        print(f"dump version:\t\t\t{info.get('dump_version')}")
                        print(f"dump migration files:\t\t{info.get('dump_migration_files')}")
                        print(f"dump django-backup-utils:\t{info.get('django_backup_utils_version')}\n")
                        print(f"current system version:\t\t{settings.BACKUP_SYSTEM_VERSION}")
                        print(
                            f"current migrations:\t\t{system_migrations_migrated} (applied) | {system_migrations_files} (files found)")
                        print(f"current django-backup-utils:\t{BackupUtilsConfig.DJANGO_BACKUP_UTILS_VERSION}")
                        print("----------------------")
        else:
            print(f"no backups have been created yet")
