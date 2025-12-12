from django_backup_utils import models


class UtilsBaseException(Exception):
    def __init__(self, message, output="", **kwargs):
        backup = kwargs.get('backup')
        params = kwargs.get('params')
        size_bytes = kwargs.get('size_bytes')
        module = kwargs.get('module')
        models.BackupLog.objects.create(message=message, output=str(output), success=False, backup=backup,
                                        module=module, params=params, size_bytes=size_bytes)
        super().__init__(message + f"\n{output}")



class CreateException(UtilsBaseException):
    pass


class LoadException(UtilsBaseException):
    pass


class UnittestFailed(UtilsBaseException):
    pass


class MigrationNotFound(Exception):
    pass


class BackupNotFound(Exception):
    pass