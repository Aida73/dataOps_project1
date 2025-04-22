from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from python_dotenv import load_dotenv
import os

load_dotenv()

DEFAULT_ADMIN_USERNAME = os.getenv('ADMIN_USERNAME')
DEFAULT_ADMIN_EMAIL = os.getenv('ADMIN_EMAIL')
DEFAULT_ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD')

class Command(BaseCommand):
    
    help = "Creating default admin account....."

    def handle(self, *args, **options):
        try:
            admin = User.objects.get(username='admin')
            self.stdout.write(
                    self.style.WARNING('Oups !! admin account already exists. Go check it ! "%s"' % admin)
                )
        except User.DoesNotExist:
            admin = User.objects.create_user(username=DEFAULT_ADMIN_USERNAME, email=DEFAULT_ADMIN_EMAIL, password=DEFAULT_ADMIN_PASSWORD)

            admin.is_staff = True
            admin.is_superuser = True

            admin.save()
        
            self.stdout.write(
                    self.style.SUCCESS('Successfully created the admin account "%s"' % admin)
                )