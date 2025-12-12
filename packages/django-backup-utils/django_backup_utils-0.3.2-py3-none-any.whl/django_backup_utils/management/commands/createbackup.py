import datetime
import json
import logging
import os
import socket
import tarfile
from pathlib import Path

from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.utils import timezone

from django_backup_utils import models
from django_backup_utils.apps import BackupUtilsConfig
from django_backup_utils.exceptions import MigrationNotFound, CreateException
from django_backup_utils.helpers import get_migration_file_list, get_system_migrations

module = str(__name__).split(".")[-1]
logger = logging.getLogger(__name__)


class Command(BaseCommand):

    def __init__(self):
        super(Command, self).__init__()

        try:
            self.migrations, self.consistent_migrations = get_migration_file_list()
        except MigrationNotFound as e:
            self.stdout.write(self.style.ERROR("there are migration files missing on your system:"))
            self.stdout.write(self.style.ERROR(str(e)))
            raise MigrationNotFound(e)

        self.created_at = datetime.datetime.now()
        self.django_time = timezone.now()  # utc

        self.dump_migration_files = 0
        self.system_migrations_migrated, self.system_migration_files = get_system_migrations()
        self.json_path = Path(os.path.join(settings.BACKUP_ROOT, BackupUtilsConfig.JSON_FILENAME))
        self.dumpinfo_path = Path(os.path.join(settings.BACKUP_ROOT, BackupUtilsConfig.DUMPINFO))
        self.context = {'system_migrations_migrated': self.system_migrations_migrated}
        self.context['module'] = module

    def make_tarfile(self, output_path: Path, compress: bool, source_dirs: list, source_files: list, migrations=[],
                     **kwargs):
        if compress:
            mode = "w:gz"
            suffix = ".tar.gz"
        else:
            mode = "w"
            suffix = ".tar"
        output_path = str(output_path) + suffix
        with tarfile.open(output_path, mode) as tar:
            for source_dir in source_dirs:
                print(f"add directory {source_dir} to tar: {output_path}")
                tar.add(source_dir, arcname=source_dir)
            for source_file in source_files:
                logger.debug(f"add file {source_file} to tar: {output_path}")
                tar.add(source_file, arcname=os.path.basename(source_file))
            for migration in migrations:
                if Path(migration).exists():
                    logger.debug(f"add file {migration} to tar: {output_path}")
                    arcname = f"_migration_backup/{migration.relative_to(settings.BASE_DIR)}"
                    tar.add(migration, arcname=arcname)
                    self.dump_migration_files += 1
        if not Path(output_path).is_file():
            raise Exception("tarfile has not been created")
        return output_path

    def make_database_dump(self, exclude=[]):
        """create database dump with dumpdata"""

        logger.debug(f"creating database dump: {self.json_path}")
        with open(self.dumpinfo_path, 'w') as f:
            f.write(f"created_at;{self.django_time}\n")
            f.write(f"dump_version;{settings.BACKUP_SYSTEM_VERSION}\n")
            f.write(f"dump_migration_files;{len(self.migrations)}\n")
            f.write(f"system_migrations_migrated;{self.system_migrations_migrated}\n")
            f.write(f"consistent_migrations;{self.consistent_migrations}\n")
            f.write(f"params;{self.context['params']}\n")
            f.write(f"backup_directories;{BackupUtilsConfig.BACKUP_DIRS}\n")
            f.write(f"django-backup-utils-version;{BackupUtilsConfig.DJANGO_BACKUP_UTILS_VERSION}")

        with open(self.json_path, 'w') as f:
            if not exclude:
                call_command("dumpdata", "--natural-foreign", "--natural-primary", stdout=f)
            else:
                logger.info(f"exclude list {exclude}")
                call_command("dumpdata", "--natural-foreign", "--natural-primary", "--exclude", *exclude, stdout=f)

        if Path(self.json_path).is_file() and Path(self.dumpinfo_path).is_file():
            return Path(self.json_path), Path(self.dumpinfo_path)
        else:
            raise Exception("Error could not create database dump")

    def add_arguments(self, parser):
        parser.add_argument('--compress', action='store_true', help="compresses backup (.gz)")
        parser.add_argument('--exclude', default=None, nargs='+', type=str,
                            help="exclude specific apps or models <appname>.<model>")
        parser.add_argument('--silent', default=None, nargs='+', type=str, help="mutes some output")

    def handle(self, compress, exclude, silent, *args, **options):
        params = json.dumps({'compress': compress, 'exclude': exclude, 'silent': silent})
        self.context['params'] = params

        OUTPUT_DIR = Path(settings.BACKUP_ROOT)

        if not silent:
            print(f"create new backup in {settings.BACKUP_ROOT}, compress = {compress}")
        if not OUTPUT_DIR.is_dir():
            logger.debug(f"creating output_dir {OUTPUT_DIR}")
            os.makedirs(OUTPUT_DIR, exist_ok=True)

        for path in BackupUtilsConfig.BACKUP_DIRS:
            posix = os.path.join(settings.BASE_DIR, path)
            posix = Path(posix)
            if not posix.is_dir():
                self.context['backup'] = "failed to create"
                raise CreateException(f"directory does not exist", output=str(posix), **self.context)

        if self.json_path.exists():
            logger.debug(f"clean up remaining {self.json_path}")
            os.remove(self.json_path)

        if self.dumpinfo_path.exists():
            logger.debug(f"clean up remaining {self.dumpinfo_path}")
            os.remove(self.dumpinfo_path)

        JSON_FILE, DUMPINFO_FILE = self.make_database_dump(exclude)
        TAR_PREFIX = str(socket.gethostname()) + "_" + BackupUtilsConfig.PROJECT_NAME + "_" + str(
            self.created_at.strftime("%Y-%m-%d_%H-%M-%S"))
        OUTPUT_TAR = Path(f"{OUTPUT_DIR}/{TAR_PREFIX}")
        OUTPUT_TAR = self.make_tarfile(output_path=OUTPUT_TAR,
                                       source_dirs=BackupUtilsConfig.BACKUP_DIRS,
                                       source_files=[JSON_FILE, DUMPINFO_FILE],
                                       migrations=self.migrations,
                                       compress=compress)

        self.context['backup'] = OUTPUT_TAR

        os.remove(Path(JSON_FILE).absolute())
        os.remove(Path(DUMPINFO_FILE).absolute())

        size_bytes = Path(OUTPUT_TAR).stat().st_size

        self.context.pop('module')
        models.Backup.objects.create(
            dump_version=settings.BACKUP_SYSTEM_VERSION,
            dump_migration_files=self.dump_migration_files,
            size_bytes=size_bytes,
            created_at=self.django_time,
            consistent_migrations=self.consistent_migrations,
            django_backup_utils_version=BackupUtilsConfig.DJANGO_BACKUP_UTILS_VERSION,
            backup_directories=str(BackupUtilsConfig.BACKUP_DIRS),
            **self.context)

        models.BackupLog.objects.create(message="created backup",
                                        module=module,
                                        success=True,
                                        size_bytes=size_bytes,
                                        backup=self.context['backup'],
                                        params=self.context['params'])

        self.stdout.write(self.style.SUCCESS(
            f"successfully created backup: {OUTPUT_TAR}, {size_bytes / 1000 / 1000} MB"))
