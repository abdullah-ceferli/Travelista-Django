from django.contrib import admin
from main.models import *
import os
from django.conf import settings
from django.template.response import TemplateResponse
from django.shortcuts import redirect
from django.contrib import messages

admin.site.register(ChatMessage)

admin.site.register(Thread)

admin.site.register(Tag)
class BlogPostTagInline(admin.TabularInline):
    model = BlogPost.tags.through 
    extra = 1 
    verbose_name = "Tag for this post"
    verbose_name_plural = "Tags for this post"


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    search_fields = ['title', 'content', 'author__name']
    list_filter = ['pub_date', 'tags']
    inlines = [BlogPostTagInline]
    exclude = ('tags',) 
    list_display = ('title', 'author', 'pub_date')
    readonly_fields = ('pub_date',)



class UserMessageAdmin(admin.ModelAdmin):
    search_fields = ['name', 'message', 'blog_post__title']
    list_filter = ['pub_date']
    list_display = ['name', 'email', 'message', 'check_box', 'pub_date']

admin.site.register(UserMessage, UserMessageAdmin)





class UserContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'surname', 'email', 'message', 'check_box']

admin.site.register(UserContact, UserContactAdmin)




class SignUpAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'phone', 'pub_date', 'ip_address']

admin.site.register(SignUp, SignUpAdmin)





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