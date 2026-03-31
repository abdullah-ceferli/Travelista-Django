from django_user_agents.utils import get_user_agent
from django.shortcuts import redirect, render
from main.models import *
from main.utils import is_message_appropriate
from django.contrib import messages
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
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        phone = request.POST.get("phone")

        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        ip_address = x_forwarded_for.split(',')[0] if x_forwarded_for else request.META.get('REMOTE_ADDR')
        
        user_agent = get_user_agent(request)
        
        if user_agent.is_mobile:
            device = "Mobile"
        elif user_agent.is_pc:
            device = "PC"
        elif user_agent.is_tablet:
            device = "Tablet"
        else:
            device = "Unknown/Bot"

        os_variant = f"{user_agent.os.family} {user_agent.os.version_string}"
        
        browser_variant = f"{user_agent.browser.family} {user_agent.browser.version_string}"

        if SignUp.objects.filter(username=username).exists():
            return render(request, self.template_name, {"error": "Username already taken."})

        try:
            email_info = validate_email(email, check_deliverability=True)
            email = email_info.normalized
        except EmailNotValidError as e:
            return render(request, self.template_name, {"error": str(e)})

        code = str(random.randint(100000, 999999))
        
        html_content = f"""
            <div style="font-family: sans-serif; text-align: center; padding: 40px; background-color: #f4f7f6;">
                <div style="max-width: 400px; margin: auto; background: white; padding: 30px; border-radius: 12px; border: 1px solid #e1e4e8;">
                    <img src="https://cdn-icons-png.flaticon.com/512/12181/12181695.png" width="70" alt="Logo">
                    <h2 style="color: #2d3436; margin-top: 20px;">Verify Your Identity</h2>
                    <p style="color: #636e72;">To keep your SpeedWager account secure, use this code:</p>
                    <div style="font-size: 36px; font-weight: bold; color: #0984e3; background: #f1f2f6; padding: 15px; border-radius: 8px; letter-spacing: 6px; margin: 25px 0;">
                        {code}
                    </div>
                    <p style="font-size: 11px; color: #b2bec3;">If you didn't request this, please change your password immediately.</p>
                </div>
            </div>
        """

        try:
            send_mail(
                'Your Verification Code',
                f"Your code is: {code}",
                'speedwagerreal2@gmail.com',
                [email],
                fail_silently=False,
                html_message=html_content,
            )
            print("\nCode sent successfully!!\n")
            print(f"Verification email sent to {email} with code: {code}\n")
        except Exception:
            return render(request, self.template_name, {"error": "Failed to send verification email."})

        request.session['temp_user'] = {
            'username': username,
            'email': email,
            'phone': phone,
            'password': encrypt_password(password),
            'code': code,
            'ip_address': ip_address,
            'device_type': device,
            'os_family': os_variant,      
            'browser_family': browser_variant 
        }
        
        return redirect('verify_page')


class VerifyView(TemplateView):
    template_name = "pages/verify.html"

    def get(self, request):
        if not request.session.get('temp_user'):
            return redirect('auth_page')
        return render(request, self.template_name)

    def post(self, request):
        temp_data = request.session.get('temp_user')
        
        if not temp_data:
            return redirect('auth_page')

        user_code = request.POST.get("code")

        if temp_data['code'] == user_code:
            SignUp.objects.create(
                username=temp_data['username'],
                email=temp_data['email'],
                phone=temp_data['phone'],
                password=temp_data['password'],
                ip_address=temp_data.get('ip_address'),
                device_type=temp_data.get('device_type'),
                os_family=temp_data.get('os_family'),     
                browser_family=temp_data.get('browser_family') 
            )
            
            del request.session['temp_user']

            return render(request, "pages/auth_page.html", {
                "success": "Verified! You can now log in !!"
            })
        
        else:
            return render(request, self.template_name, {"error": "Invalid code. Please check your inbox."})

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
