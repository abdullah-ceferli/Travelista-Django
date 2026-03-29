from django.shortcuts import redirect, render
from main.models import *
from main.utils import is_message_appropriate
from django.contrib import messages
import math
from django.utils import timezone
import random
from django.core.mail import send_mail
from email_validator import validate_email, EmailNotValidError
from main.utils import encrypt_password, decrypt_password
from main.serializers import *
from django.views.generic import TemplateView
# Create your views here.


class HomeView(TemplateView):
    template_name = 'pages/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        items = UserContact.objects.filter(check_box=True).order_by('-pub_date')[:8]
        count = items.count()
        num_dots = (count // 2) + 1 if count > 0 else 0
        
        context['carousel_items'] = items
        context['dots_range'] = range(num_dots) 
        
        return context


class AboutView(TemplateView):
    template_name = 'pages/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        items = UserContact.objects.filter(check_box=True).order_by('-pub_date')[:8]
        count = items.count()
        num_dots = (count // 2) + 1 if count > 0 else 0
        
        context['carousel_items'] = items
        context['dots_range'] = range(num_dots) 
        
        return context


class PackagesView(TemplateView):
    template_name = 'pages/packages.html'


class HotelsView(TemplateView):
    template_name = 'pages/hotels.html'


class BlogHomeView(TemplateView):
    template_name = 'pages/blog-home.html'


class BlogSingleView(TemplateView):
    template_name = 'pages/blog-single.html'

    def get(self, request):
        context = self.get_context_data()
        return render(request, self.template_name, context)

    def post(self, request):
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")
        subject = request.POST.get("subject")
        user_img = request.FILES.get("user_img")

        full_content = f"{name} {email} {message}"
        if not is_message_appropriate(full_content):
            context = self.get_context_data()
            context.update({
                "error": "Message blocked! Please do not use inappropriate language.",
                "name": name,
                "email": email,
                "subject": subject,
                "message": message,
            })
            return render(request, self.template_name, context)

        UserMessage.objects.create(
            name=name,
            email=email,
            message=message,
            user_img=user_img,
            subject=subject,
        )

        messages.success(request, "Thank you for your comment!")
        return redirect('index')


class ContactView(TemplateView):
    template_name = 'pages/contact.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        # Data extraction
        name = request.POST.get("name")
        surname = request.POST.get("surname")
        email = request.POST.get("email")
        subject = request.POST.get("subject")
        message = request.POST.get("message")
        user_img = request.FILES.get("user_img")
        stars = request.POST.get("stars", 5)

        full_content = f"{subject} {message}"

        # Custom validation logic
        if not is_message_appropriate(full_content):
            context = {
                "error": "Message blocked! Please do not use inappropriate language.",
                "name": name, "surname": surname, "email": email,
                "subject": subject, "message": message,
            }
            return render(request, self.template_name, context)

        # IP Address logic
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        ip_address = x_forwarded_for.split(',')[-1].strip() if x_forwarded_for else request.META.get('REMOTE_ADDR')

        # Object creation
        UserContact.objects.create(
            name=name,
            surname=surname,
            email=email,
            subject=subject,
            message=message,
            user_img=user_img,
            stars=stars,
            ip_address=ip_address,
            pub_date=timezone.now()
        )

        messages.success(request, "Thank you! Your message has been sent.")
        return redirect('index')


class ElementsView(TemplateView):
    template_name = 'pages/elements.html'


class InsuranceView(TemplateView):
    template_name = 'pages/insurance.html'


class ProfileView(TemplateView):
    template_name = 'pages/profile.html'


class AuthView(TemplateView):
    template_name = "pages/auth_page.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        form_type = request.POST.get("form_type")

        if form_type == "signup":
            return self.handle_signup(request)
        
        return render(request, self.template_name)

    def handle_signup(self, request):
        """Internal logic for the signup process."""
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        phone = request.POST.get("phone")

        if SignUp.objects.filter(username=username).exists():
            return render(request, self.template_name, {"error": "Username already taken."})

        if SignUp.objects.filter(email=email).exists():
            return render(request, self.template_name, {"error": "Email already registered."})

        try:
            email_info = validate_email(email, check_deliverability=True)
            email = email_info.normalized
        except EmailNotValidError as e:
            return render(request, self.template_name, {"error": str(e)})

        code = str(random.randint(100000, 999999))
        try:
            send_mail(
                'Your Verification Code',
                f'Your code is: {code}',
                'speedwagerreal2@gmail.com',
                [email],
                fail_silently=False,
            )
        except Exception as e:
            print(f"SMTP Error: {e}")
            return render(request, self.template_name, {"error": "We couldn't send the code. Please check your email address."})

        secure_password = encrypt_password(password) 
        request.session['temp_user'] = {
            'username': username,
            'email': email,
            'phone': phone,
            'password': secure_password,
            'code': code
        }
        
        return redirect('verify_page')


class VerifyView(TemplateView):
    template_name = "pages/verify.html"

    def get_temp_data(self, request):
        """Helper to retrieve session data or return None."""
        return request.session.get('temp_user')

    def get(self, request):
        if not self.get_temp_data(request):
            return redirect('auth_page')
        
        return render(request, self.template_name)

    def post(self, request):
        temp_data = self.get_temp_data(request)
        
        if not temp_data:
            return redirect('auth_page')

        user_code = request.POST.get("code")

        if temp_data['code'] == user_code:
            SignUp.objects.create(
                username=temp_data['username'],
                email=temp_data['email'],
                phone=temp_data['phone'],
                password=temp_data['password']
            )
            
            del request.session['temp_user']

            return render(request, "pages/auth_page.html", {
                "success": "Account Verified and Created!"
            })
        
        else:
            return render(request, self.template_name, {"error": "Wrong code!"})


def create_google_user_profile(sender, instance, created, **kwargs):
    if created:
        if not SignUp.objects.filter(email=instance.email).exists():
            SignUp.objects.create(
                username=instance.username,
                email=instance.email,
                password="GOOGLE_AUTH_USER",
                phone="N/A",
                pub_date=timezone.now()
            )
