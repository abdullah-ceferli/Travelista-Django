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

    path('blog/<int:pk>/', BlogSingleView.as_view(), name='blog-single'),

    path('auth_page/', AuthView.as_view(), name='auth_page'),

    path('profile/', ProfileView.as_view(), name='profile'),

    path('verify_page/', VerifyView.as_view(), name='verify_page'),

    path('logout/', LogoutView.as_view(), name='logout_action'),

    path('setup_profile/', SetupProfileView.as_view(), name='setup_profile'),

    path('add_blog/', AddBlogView.as_view(), name='add_blog'),

    path('category/<int:tag_id>/', CategoryDetailView.as_view(), name='category-detail'),

    path('connect/', ConnectsView.as_view(), name='connect'),
]
