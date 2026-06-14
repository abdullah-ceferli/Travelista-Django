import os
import shutil
from django.core.management.base import BaseCommand
from django.conf import settings
from django.apps import apps
from django.db.models import FileField

class Command(BaseCommand):
    help = 'Moves unused media files to a trash folder'

    def handle(self, *args, **kwargs):
        trash_dir = os.path.join(settings.BASE_DIR, 'bin')
        os.makedirs(trash_dir, exist_ok=True)
        
        media_root = os.path.normpath(settings.MEDIA_ROOT)
        used_files = set()

        self.stdout.write("Scanning database for used media files...")

        for model in apps.get_models():
            file_fields = [f for f in model._meta.fields if isinstance(f, FileField)]
            
            if file_fields:
                for field in file_fields:
                    paths = model.objects.exclude(**{f"{field.name}__exact": ''}).values_list(field.name, flat=True)
                    for path in paths:
                        if path:
                            full_path = os.path.normpath(os.path.join(media_root, path))
                            used_files.add(full_path)

        self.stdout.write(f"Found {len(used_files)} files actively used in the database.")
        self.stdout.write("Scanning media folder for unused files...")

        moved_count = 0

        for root, dirs, files in os.walk(media_root):
            for file in files:
                file_path = os.path.normpath(os.path.join(root, file))
                
                if file_path not in used_files:
                    rel_path = os.path.relpath(file_path, media_root)
                    dest_path = os.path.join(trash_dir, rel_path)
                    
                    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                    
                    shutil.move(file_path, dest_path)
                    moved_count += 1
                    self.stdout.write(self.style.WARNING(f"Moved to trash: {rel_path}"))

        self.stdout.write(self.style.SUCCESS(f"Cleanup complete! Moved {moved_count} unused files to {trash_dir}."))