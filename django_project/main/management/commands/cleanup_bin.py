import os
import shutil
from django.core.management.base import BaseCommand
from django.conf import settings

class Command(BaseCommand):
    help = 'Permanently deletes all files inside the project-trash-img directory'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Delete files without asking for confirmation',
        )

    def handle(self, *args, **options):
        trash_dir = os.path.join(settings.BASE_DIR, 'bin')

        if not os.path.exists(trash_dir) or not os.listdir(trash_dir):
            self.stdout.write(self.style.SUCCESS("The trash bin is already empty."))
            return

        if not options['force']:
            confirm = input(f"Are you sure you want to PERMANENTLY delete everything in {trash_dir}? (y/N): ")
            if confirm.lower() != 'y':
                self.stdout.write(self.style.WARNING("Cleanup cancelled."))
                return

        count = 0
        for root, dirs, files in os.walk(trash_dir):
            for file in files:
                os.remove(os.path.join(root, file))
                count += 1
        
        for root, dirs, files in os.walk(trash_dir, topdown=False):
            for name in dirs:
                os.rmdir(os.path.join(root, name))

        self.stdout.write(self.style.SUCCESS(f"Successfully deleted {count} files permanently."))