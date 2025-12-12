# Django Backup Utils

**django-backup-utils** offers a very bare-bone solution for managing backup/restore in your Django projects.  
It is based on default django commands such as "dumpdata" and "loaddata".

## DISCLAIMER:
django-backup-utils is designed to help in dev environments, when migration files are possibly not yet committed to VCS.  
**I do not recommend it for use in productive environments.**  



### What this package provides:

- Create backups with or without compression (tar/tar:gz)
- Restore database backup
- Restore migration files (only if specified)
- Backup and restore any directory on your system, for example ```"./media"```, or ```"/tmp/hello_world/"```
- Manage backups/restoration through the Django admin interface
- Verify migrations are consistent with the current migration recorder

### Backup Contents

Each backup includes:

- A timestamp
- A full database dump in JSON format (using `dumpdata`) by default
- All `.py` migration files that are currently migrated (if found)
- A customizable version stamp (e.g., a commit hash)
- Identifiers such as hostname and Django project name

### Restoration Features

When restoring from a backup, you can:

- Automatically retrieve the latest backup for your host and project
- View the backup’s version stamp alongside the current version
- See differences between backup migrations and current migrations (file count / missing files)
- Run a blank unittest (done by default) to ensure that the fixture can be loaded (via "loaddata") before making changes

All backup logs are stored in the database. You can manage backups, including creation, synchronization, and restoration, via the Django admin interface.


## Quick Start

1. Install the package:

   ```bash
   $ pip install django-backup-utils
   ```

2. Update `settings.py`:

   ```python
   INSTALLED_APPS = [
     ...
     'django_backup_utils.apps.BackupUtilsConfig',
   ]

   BACKUP_ROOT = "/my/path/to/backupdir/"
   BACKUP_SYSTEM_VERSION = "my_build_id"
   APPS_DIR = BASE_DIR  # Change this accordingly if you use for example django-cookiecutter
   ```

   - `BACKUP_ROOT`: Directory where your backups will be stored.
   - `BACKUP_SYSTEM_VERSION`: Identification tag for your backup (e.g., git commit hash or tag).
   - `APPS_DIR`: Where your django-apps are located.


   Optional settings:

   - `BACKUP_DIRS = []` (Default = []): Specifies additional directories to include in the backup.
   - `BACKUP_IGNORE_CONSISTENCY = True` (Default = False): Ignores inconsistencies between the MigrationRecorder and local migration files. By default, backups with inconsistent migrations raise a `MigrationNotFound` exception.

3. Update `urls.py`:

   ```python
   from django.urls import path, include

   urlpatterns = [
     ...
     path('backup/', include('django_backup_utils.urls')),
   ]
   ```

4. Run migrations:

   ```bash
   $ python3 manage.py migrate
   ```

## Usage

- **Create a Backup**:

   ```bash
   $ python3 manage.py createbackup
   ```

   Optional arguments:
   - `--compress`: Compresses the backup (.gz).
   - `--exclude`: Exclude specific apps or models (`<appname>.<model>`).
   - `--silent`: Mutes some output.


- **Restore a Backup**:

   ```bash
   $ python3 manage.py loadbackup
   ```

   Optional arguments:
   - `--tarpath`: Load the specified backup tar file.
   - `--flush`: Flush the database (delete existing data).
   - `--deletedirs`: Delete all directories specified in `settings.BACKUP_DIRS` before restoring.
   - `--loadmigrations`: Restore migration files.
   - `--skiptest`: Skip the unittest for loading the database dump.


- **List Available Backups**:

   ```bash
   $ python3 manage.py listbackups
   ```

   Optional arguments:
   - `--hostname`: Show backups for a specific hostname.
   - `--projectname`: Show backups for a specific Django project.
   - `--all`: Show all backups.
   - `--showinfo`: Display backup metadata.
   - `--showlatest`: Show only the latest backup.


- **Synchronize Backups**:

   ```bash
   $ python3 manage.py syncbackups
   ```
   Checks your ``BACKUP_ROOT`` and synchronizes it with DB

   Optional arguments:
   - `--silent`: Mutes some output.


## Admin Interface Overview

- **System Migrations**: Displays the number of migrations currently applied (from the MigrationRecorder).
- **System Migration Files**: Shows the current number of local migration files.
- **Current System Version**: Displays the current `BACKUP_SYSTEM_VERSION`.

Each Backup object includes:

- **Consistent Migrations**: `True` if MigrationRecorder matches local migration files.
- **System Migrations (At dump time)**: Number of system migrations when the dump was created.
- **Dump Migration Files**: Number of migration files archived in the dump.

### Permissions

- **Restore Backups**:  
  `django_backup_utils | can_restore_backup`
  
- **Create/Synchronize Backups**:  
  `django_backup_utils | can_add_backup`
