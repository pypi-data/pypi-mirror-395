from django.db import models


class MainAttributes(models.Model):
    backup = models.TextField()
    params = models.TextField(null=True, blank=True)
    size_bytes = models.BigIntegerField(null=True, blank=True)

    class Meta:
        abstract = True


class Backup(MainAttributes):
    dump_version = models.TextField(null=True, blank=True)
    system_migrations_migrated = models.IntegerField("System Migrations (at dump time)", null=True, blank=True)
    dump_migration_files = models.IntegerField("Dump Migration Files", null=True, blank=True)
    created_at = models.DateTimeField()
    consistent_migrations = models.BooleanField("Consistent Migrations", default=False)
    django_backup_utils_version = models.CharField("django-backup-utils version", max_length=10, null=True, blank=True)
    backup_directories = models.TextField(null=True, blank=True)
    # inconsistent migrations occur if your migration recorder does not match your local migration files

    def __str__(self):
        return f"Backup {self.pk}"

    class Meta:
        permissions = (
            ("can_restore_backup", "Can restore backup"),
        )


class BackupLog(MainAttributes):
    message = models.CharField(max_length=200)
    module = models.CharField(max_length=200)
    output = models.TextField(null=True, blank=True)
    success = models.BooleanField(default=False)
    executed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"BackupLog {self.pk}"
