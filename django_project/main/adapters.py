from allauth.account.adapter import DefaultAccountAdapter
from .models import SignUp
from django.utils import timezone

class MyCustomAdapter(DefaultAccountAdapter):
    def get_login_redirect_url(self, request):
        django_user = request.user
        
        signup_user, created = SignUp.objects.get_or_create(
            email=django_user.email,
            defaults={
                'username': django_user.username,
                'password': "GOOGLE_USER",
                'phone': "0000000000",
                'pub_date': timezone.now()
            }
        )

        request.session['user_id'] = signup_user.id
        request.session['username'] = signup_user.username

        if not signup_user.name:
            return '/pages/setup_profile/'
        
        return '/'