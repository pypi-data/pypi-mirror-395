import logging
import os
from pathlib import Path

from django.conf import settings
from django.contrib import admin
from django.contrib import messages
from django.urls import reverse_lazy
from django.utils.safestring import mark_safe

from django_backup_utils import models, helpers
from django_backup_utils.apps import BackupUtilsConfig

logger = logging.getLogger(__name__)


class BackupLogAdmin(admin.ModelAdmin):
    list_filter = ("module",)
    list_display = (
        "pk", "module", "message", "backup", "size_mb", "success", "executed_at",)
    readonly_fields = ("module", "message", "backup", "size_bytes", "success", "executed_at", "params", "output",)

    def has_add_permission(self, request, obj=None):
        return False

    def restore_link(self, obj):
        if obj.module == "createbackup":
            return mark_safe(f'<a href="{reverse_lazy("restore-backup", kwargs={"pk": obj.pk})}">restore</a>')

    def size_mb(self, obj):
        if obj.size_bytes:
            return f"{round(float(obj.size_bytes / 1000 / 1000), 2)} MB"
        return ""


class BackupAdmin(admin.ModelAdmin):
    list_display = (
        "pk", "backup", "size_mb", "created_at", "backup_directories", "dump_version", "consistent_migrations",
        "restore_link",
        "system_migrations_migrated",
        "dump_migration_files", "django_backup_utils_version")

    readonly_fields = (
        "backup", 'size_bytes', "created_at", "backup_directories", "dump_version", "consistent_migrations",
        "system_migrations_migrated",
        "dump_migration_files", "params", "django_backup_utils_version")
    list_display_links = ("pk", "restore_link",)

    change_list_template = "django_backup_utils/backup_changelist.html"
    ordering = ("-created_at",)

    def changelist_view(self, request, extra_context=None):
        self.current_system_migrations_migrated, self.migration_files_found = helpers.get_system_migrations()

        extra_context = {'system_migrations_migrated': self.current_system_migrations_migrated,
                         'system_migration_files_found': self.migration_files_found,
                         'ignore_consistency': BackupUtilsConfig.BACKUP_IGNORE_CONSISTENCY,
                         'backup_system_version': settings.BACKUP_SYSTEM_VERSION,
                         'backup_dirs': settings.BACKUP_DIRS,
                         'django_backup_utils_version': BackupUtilsConfig.DJANGO_BACKUP_UTILS_VERSION}
        return super(BackupAdmin, self).changelist_view(request, extra_context)

    def has_add_permission(self, request, obj=None):
        return False

    def restore_link(self, obj):
        return mark_safe(f'<a href="{reverse_lazy("restore-backup", kwargs={"pk": obj.pk})}">restore</a>')

    def size_mb(self, obj):
        if obj.size_bytes:
            return f"{round(float(obj.size_bytes / 1000 / 1000), 4)} MB"
        return ""

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            backup = Path(obj.backup)
            if backup.is_file():
                os.remove(backup)
                logger.info(f"-> deleted file {backup}")
                models.BackupLog.objects.create(message="deleted backup", module="admin:backup_delete",
                                                output=f"deleted {backup}",
                                                backup=obj.backup,
                                                size_bytes=obj.size_bytes,
                                                success=True)
                messages.success(request, f'deleted {obj.backup}')
            else:
                models.BackupLog.objects.create(message="deleted backup object", module="admin:backup_delete",
                                                output=f"backup file was not found",
                                                backup=obj.backup, )
                messages.info(request, f'deleted only object {obj}; ({obj.backup} was not found)')
            obj.delete()


admin.site.register(models.Backup, BackupAdmin)
admin.site.register(models.BackupLog, BackupLogAdmin)
