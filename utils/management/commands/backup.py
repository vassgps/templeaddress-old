#webapp/utils/management/commands/backup.py
import os
import subprocess
from django.core.management.base import BaseCommand
from django.conf import settings

class Command(BaseCommand):
    help = 'Backup the database to a file'

    def handle(self, *args, **options):
        db_name = settings.DATABASES['default']['NAME']
        db_user = settings.DATABASES['default']['USER']
        db_password = settings.DATABASES['default']['PASSWORD']
        db_host = settings.DATABASES['default']['HOST']
        db_port = settings.DATABASES['default']['PORT']

        backup_file = os.path.join(settings.BASE_DIR, 'db_backup.sql')

        os.environ['PGPASSWORD'] = db_password

        try:
            # Execute the pg_dump command
            subprocess.check_call([
                'pg_dump',
                '-h', db_host,
                '-p', str(db_port),
                '-U', db_user,
                '-F', 'c',
                '-f', backup_file,
                db_name
            ])
            self.stdout.write(self.style.SUCCESS(f'Database backup successful: {backup_file}'))
        except subprocess.CalledProcessError as e:
            self.stderr.write(self.style.ERROR(f'Error during database backup: {e}'))
        finally:
            del os.environ['PGPASSWORD']