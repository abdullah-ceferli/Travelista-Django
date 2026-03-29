from django.urls import path
from main.views import *

urlpatterns = [
    path('index/', HomeView.as_view(), name='index'),

    path('contact/', ContactView.as_view(), name='contact'),

    path('about/', AboutView.as_view(), name='about'),

    path('elements/', ElementsView.as_view(), name='elements'),

    path('hotels/', HotelsView.as_view(), name='hotels'),

    path('insurance/', InsuranceView.as_view(), name='insurance'),

    path('packages/', PackagesView.as_view(), name='packages'),

    path('blog-home/', BlogHomeView.as_view(), name='blog-home'),

    path('blog-single/', BlogSingleView.as_view(), name='blog-single'),

    path('auth_page/', AuthView.as_view(), name='auth_page'),

    path('profile/', ProfileView.as_view(), name='profile'),

    path('verify_page/', VerifyView.as_view(), name='verify_page'),
]
