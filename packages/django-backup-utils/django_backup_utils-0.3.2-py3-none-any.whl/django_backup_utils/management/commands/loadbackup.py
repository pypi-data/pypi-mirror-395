import io
import json
import logging
import os
import shutil
import tarfile
import unittest
from contextlib import redirect_stdout
from django.conf import settings
from django.core import management
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from pathlib import Path

from django_backup_utils import models
from django_backup_utils.apps import BackupUtilsConfig
from django_backup_utils.exceptions import MigrationNotFound, LoadException, UnittestFailed
from django_backup_utils.helpers import get_migration_file_list, get_system_migrations, extract_dumpinfo, \
    get_backup_list_by_time
from django_backup_utils.tests import loaddata

module = str(__name__).split(".")[-1]
logger = logging.getLogger(__name__)


def open_tar(input_filename):
    if str(input_filename).endswith("tar.gz"):
        tar = tarfile.open(input_filename, "r:gz")
    elif str(input_filename).endswith("tar"):
        tar = tarfile.open(input_filename, "r:")
    return tar


def extract_tar(input_filename, member_path="", dir="", strip=0, checkonly=False):
    tar = open_tar(input_filename)
    if member_path:
        for member in tar.getmembers():
            if member_path:
                if member_path in member.name:
                    if not strip <= 0:
                        p = Path(member.path)
                        member.path = p.relative_to(*p.parts[:strip])
                    if not checkonly:
                        logger.debug(f"extract file ->./{member_path}")
                        tar.extract(member, settings.BASE_DIR)
                        logger.debug(f"extracted {member.name} to {settings.BASE_DIR}")
    elif dir:
        absolute = False
        if Path(dir).is_absolute():
            absolute = True
        for member in tar.getmembers():
            dir_member = []
            if member.name in dir:
                logger.debug(f"found BACKUP_DIR in backup {dir}")
                if not checkonly:
                    dir_member.append(member)
                    submembers = tar.getmembers()
                    for submember in submembers:
                        if str(submember.name).startswith(member.name):
                            dir_member.append(submember)
                    if not absolute:
                        logger.debug(f"relative extract ->: {Path(dir)}")
                        tar.extractall(members=dir_member, path=settings.BASE_DIR)
                    else:
                        # todo future feature
                        outpath = Path(dir)
                        logger.debug(f"absolute extract ->: {outpath}")
                        tar.extractall(members=dir_member, path=Path("/").root)

    tar.close()


def check_member(input_filename, member_path, strip=0):
    logger.debug(f"check for data in backup... {member_path}")
    tar = open_tar(input_filename)
    for member in tar.getmembers():
        if member.name in member_path:
            return member.name


def load_database_dump(filepath, **kwargs):
    logger.debug(f"loading backup fixture {filepath.name}...")
    stdout_capture = io.StringIO()
    with redirect_stdout(stdout_capture):
        management.call_command("loaddata", filepath, verbosity=1)
    output = stdout_capture.getvalue()
    if not "Installed" in output:
        raise LoadException(message=f"load_database_dump has failed", output=output, **kwargs)
    else:
        logger.debug(output)


def flush_db():
    management.call_command("sqlflush", verbosity=1)  # for debugging if flush is not working
    management.call_command("flush", verbosity=1, interactive=False)


def delete_dir(dir, **kwargs):
    dir = Path(dir)
    if dir.exists():
        shutil.rmtree(dir)
    if dir.exists():
        raise LoadException(message=f"directory could not be deleted", output=dir, **kwargs)
    else:
        logger.debug(f"deleted directory {dir}")


def create_input():
    inp = input("continue y/N ? ")
    if str(inp) == "y" or str(inp) == "yes":
        return True


class Command(BaseCommand):

    def __init__(self):
        self.migrations = None
        self.migration_not_found = None
        try:
            self.migrations, self.consistent_migrations = get_migration_file_list()
        except MigrationNotFound as e:
            self.migration_not_found = str(e)

        self.json_path = Path(os.path.join(settings.BASE_DIR, BackupUtilsConfig.JSON_FILENAME))
        self.dumpinfo_path = Path(os.path.join(settings.BASE_DIR, BackupUtilsConfig.DUMPINFO))
        self.system_migrations_migrated, self.system_migration_files = get_system_migrations()
        self.context = {'system_migrations_migrated': self.system_migrations_migrated}
        self.context['system_migration_files'] = None
        self.context['system_version'] = settings.BACKUP_SYSTEM_VERSION
        self.context['module'] = module
        super(Command, self).__init__()

    def add_arguments(self, parser):
        parser.add_argument('--tarpath', type=str, help='load the specified backup tarfile')
        parser.add_argument('--flush', action='store_true', help='flush the database (delete existing data)')
        parser.add_argument('--deletedirs', action='store_true',
                            help='delete all directories specified in settings.BACKUP_DIRS (before restoring)')
        parser.add_argument('--noinput', action='store_true', help='disable all prompts')
        parser.add_argument('--loadmigrations', action='store_true', help='restore all migration files')
        parser.add_argument('--skiptest', action='store_true', help='skip the unittest for loading database dump')
        parser.add_argument('--silent', action='store_true', help='mutes some output')

    def handle(self, tarpath, flush, deletedirs, noinput, loadmigrations, skiptest, silent, *args, **options):

        params = json.dumps(
            {"flush": flush, "deletedirs": deletedirs, "noinput": noinput, "loadmigrations": loadmigrations,
             "skiptest": skiptest, 'silent': silent})
        self.context['params'] = params

        if not tarpath:
            sorted_backups = get_backup_list_by_time(settings.BACKUP_ROOT)
            if not sorted_backups:
                print("nothing to load")
                return
            tar = sorted_backups[-1].get('path')
            if tar:
                tarpath = Path(tar)
                if not silent:
                    print(f"loading latest backup: \t\t {tarpath}")
            else:
                if not silent:
                    print("nothing to load")
                return
        else:
            tarpath = Path(tarpath)
            if not silent:
                print(f"loading given backup: \t\t {tarpath}")

        self.context['backup'] = tarpath
        info = extract_dumpinfo(str(tarpath))
        self.context['dump_version'] = info['dump_version']
        self.context['system_migration_files'] = self.system_migration_files
        size = Path(tarpath).stat().st_size
        self.context['size_bytes'] = size
        time = parse_datetime(info.get('created_at'))

        if not silent:
            print(f"created at:\t\t\t {time.astimezone(tz=timezone.get_current_timezone())}")
            print(f"size:\t\t\t\t {round(float(size / 1000 / 1000), 4)} MB")
            print(f"backup directories:   \t\t {info['backup_directories']}")
            print(f"dump-version:         \t\t {self.context['dump_version']}")
            print(f"system-version (now): \t\t {self.context['system_version']}")
            print(f"dump-migration-files: \t\t {info['dump_migration_files']} (files)")
            print(
                f"system-migrations (now):\t {self.system_migration_files} (files) / {self.context['system_migrations_migrated']} (applied by MigrationRecorder)")
            print(f"dump django-backup-utils: \t {info['django_backup_utils_version']}")
            print(f"now django-backup-utils: \t {BackupUtilsConfig.DJANGO_BACKUP_UTILS_VERSION}")
            print()
        if not loadmigrations:
            if self.migration_not_found:
                self.stdout.write(self.style.ERROR("there are migration files missing on your system:"))
                self.stdout.write(self.style.ERROR(self.migration_not_found))
                members = []
                for migration in str(self.migration_not_found).split("\n"):
                    member = check_member(tarpath, f"_migration_backup/{migration}")
                    if member:
                        members.append(migration)
                if members:
                    if not silent:
                        print(f"this backup also contains:")
                    for each in members:
                        print("\t" + each)
                    if not silent:
                        print("\n use parameter --loadmigrations to restore them")
                text = f"Migration {self.migration_not_found} was not found;"
                if members:
                    text += f"however this backup contains {members}, you can restore them via --loadmigrations"
                raise MigrationNotFound(text)

        if not noinput:
            result = create_input()
            if not result:
                if not silent:
                    print("abort")
                return

        if not tarpath.is_file():
            raise Exception(f"file {tarpath} does not exist")

        if loadmigrations:
            extract_tar(str(tarpath), "_migration_backup", strip=1)

        extract_tar(tarpath, member_path=BackupUtilsConfig.JSON_FILENAME)

        if not skiptest:
            verbosity = 3
            if silent:
                verbosity = 0
            print()
            logger.debug(f"running database restore test ...\n")
            suite = unittest.defaultTestLoader.loadTestsFromTestCase(loaddata.TestMigration)
            result = unittest.TextTestRunner(verbosity=verbosity).run(suite)

            if result.errors:
                logger.error(f"failed unittest:\n{result.errors}")
                raise UnittestFailed(message=f"unittest failed", output=str(result.errors[0]), **self.context)

        if flush:
            flush_db()

        load_database_dump(self.json_path, **self.context)

        if deletedirs:
            logger.debug(f"trying to delete {BackupUtilsConfig.BACKUP_DIRS}...")
            for dir in BackupUtilsConfig.BACKUP_DIRS:
                delete_dir(dir, **self.context)

        # restore backup_dirs
        for each in BackupUtilsConfig.BACKUP_DIRS:
            extract_tar(tarpath, dir=each)

        logger.debug(f"removing {self.json_path}")
        os.remove(self.json_path)

        if not self.json_path.exists():
            self.stdout.write(self.style.SUCCESS(f"successfully restored backup: {tarpath}"))
            models.BackupLog.objects.create(message="loaded backup",
                                            module=module,
                                            success=True,
                                            size_bytes=self.context['size_bytes'],
                                            backup=self.context['backup'],
                                            params=self.context['params'])
