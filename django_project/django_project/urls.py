"""
URL configuration for django_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from main.apiViews import *
from django.conf import settings
from django.views.static import serve
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('pages/', include('main.urls')),
    path('accounts/', include('allauth.urls')),

    # api endpoints
    path('api/destinations/', DestinationListAPI.as_view(), name='destination-list-api'),
    path('api/user-contacts/', UserContactListAPI.as_view(), name='user_contacts_api'),
    path('api/hotels/', HotelsListAPI.as_view(), name='hotels_api'),
    path('api/user-messages/', UserMessageListAPI.as_view(), name='user-messages-api'),
    path('api/user-data/', UserDataListAPI.as_view(), name='user-data-api'),
    path('api/posts/', BlogPostListAPI.as_view(), name='post-list-api'),
    path('api/get-or-create-thread/<int:target_user_id>/', GetOrCreateThread.as_view(), name='get_thread'),
    path('api/messages/send/', SendMessageAPI.as_view(), name='send_message'),
    path('api/messages/<int:thread_id>/', MessageListAPI.as_view(), name='message_list'),
]



if not settings.DEBUG:
    urlpatterns += [
        re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
        re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    ]

else:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
