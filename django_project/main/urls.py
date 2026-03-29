from django.urls import path
from main.views import *

urlpatterns = [
    path('index/', HomeView.as_view(), name='index'),

    path('contact/', contact, name='contact'),

    path('about/', AboutView.as_view(), name='about'),

    path('elements/', elements, name='elements'),

    path('hotels/', hotels, name='hotels'),

    path('insurance/', insurance, name='insurance'),

    path('packages/', packages, name='packages'),

    path('blog-home/', blogHome, name='blog-home'),

    path('blog-single/', blogSingle, name='blog-single'),

    path('auth_page/', auth_page, name='auth_page'),

    path('profile/', profile, name='profile'),

    path('verify_page/', verify_page, name='verify_page'),
]
