from allauth.account.adapter import DefaultAccountAdapter
from .models import SignUp
from django.utils import timezone

class MyCustomAdapter(DefaultAccountAdapter):
    def get_login_redirect_url(self, request):
        django_user = request.user
        
        # 1. Sync Google User to your SignUp model
        # 'created' will be True if this is their first time ever
        signup_user, created = SignUp.objects.get_or_create(
            email=django_user.email,
            defaults={
                'username': django_user.username,
                'password': "GOOGLE_USER",
                'phone': "0000000000",
                'pub_date': timezone.now()
            }
        )

        # 2. Log them into your CUSTOM session system
        request.session['user_id'] = signup_user.id
        request.session['username'] = signup_user.username

        # 3. Check if they need to fill out the Profile GUI
        # If 'name' is empty, they haven't finished the setup_profile page yet
        if not signup_user.name:
            return '/pages/setup_profile/'
        
        # If they already have a name, just go home
        return '/'