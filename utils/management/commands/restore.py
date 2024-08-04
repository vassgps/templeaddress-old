#webapp/utils/management/commands/restore.py
import os
import subprocess
from django.core.management.base import BaseCommand
from django.conf import settings

class Command(BaseCommand):
    help = 'Restore the database from a backup file'

    def handle(self, *args, **options):
        db_name = settings.DATABASES['default']['NAME']
        db_user = settings.DATABASES['default']['USER']
        db_password = settings.DATABASES['default']['PASSWORD']
        db_host = settings.DATABASES['default']['HOST']
        db_port = settings.DATABASES['default']['PORT']
        
        backup_file = os.path.join(settings.BASE_DIR, 'db_backup.sql')
        
        os.environ['PGPASSWORD'] = db_password
        
        try:
            subprocess.check_call([
                'psql',
                '-h', db_host,
                '-p', str(db_port),
                '-U', db_user,
                '-d', db_name,
                '-f', backup_file
            ])
            self.stdout.write(self.style.SUCCESS('Database restored successfully'))
        except subprocess.CalledProcessError as e:
            self.stderr.write(self.style.ERROR(f'Error restoring database: {e}'))
        finally:
            del os.environ['PGPASSWORD']
