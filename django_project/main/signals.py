from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import SignUp  
from django.utils import timezone

@receiver(post_save, sender=User)
def save_to_custom_signup_model(sender, instance, created, **kwargs):
    if created:
        if not SignUp.objects.filter(email=instance.email).exists():
            SignUp.objects.create(
                username=instance.username,
                email=instance.email,
                password="GOOGLE_USER", 
                phone="0000000000",     
                pub_date=timezone.now()
            )