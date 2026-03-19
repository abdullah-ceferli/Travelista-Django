from django.contrib import admin
from main.models import *
import os
from django.conf import settings
from django.template.response import TemplateResponse
from django.shortcuts import redirect
from django.contrib import messages

# Register your models here.

admin.site.register(UserMessage)

class HotelAmenityInline(admin.TabularInline):
    model = HotelAmenity
    extra = 1 

class DestinationAmenityInline(admin.TabularInline):
    model = DestinationsAmenity
    extra = 1 

@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ['name', 'stars', 'price_per_night']
    inlines = [HotelAmenityInline] 

@admin.register(Destinations)
class DestinationsAdmin(admin.ModelAdmin):
    list_display = ['name', 'location']
    inlines = [DestinationAmenityInline] 

@admin.register(TrashBin)
class TrashBinAdmin(admin.ModelAdmin):
    
    def changelist_view(self, request, extra_context=None):
        trash_dir = os.path.join(settings.BASE_DIR, 'bin')
        
        if request.method == 'POST' and 'delete_all' in request.POST:
            count = 0
            if os.path.exists(trash_dir):
                for root, dirs, files in os.walk(trash_dir):
                    for file in files:
                        os.remove(os.path.join(root, file))
                        count += 1
            messages.success(request, f"Successfully permanently deleted {count} files from the trash bin.")
            return redirect(request.path)

        trashed_files = []
        if os.path.exists(trash_dir):
            for root, dirs, files in os.walk(trash_dir):
                for file in files:
                    full_path = os.path.join(root, file)
                    rel_path = os.path.relpath(full_path, trash_dir)
                    trashed_files.append({
                        'name': rel_path,
                        'size': round(os.path.getsize(full_path) / 1024, 2)  
                    })
        
        context = dict(
            self.admin_site.each_context(request),
            title="Orphaned Media Trash Bin",
            trashed_files=trashed_files,
            opts=self.model._meta, 
        )
        return TemplateResponse(request, "admin/trash_bin_list.html", context)