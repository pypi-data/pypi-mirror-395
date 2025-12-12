from django.test import TestCase

from django_backup_utils.apps import BackupUtilsConfig

class TestMigration(TestCase):

    fixtures = [BackupUtilsConfig.JSON_FILENAME]

    def test_loaddata(self):
        """Installs the fixture in fresh test database"""