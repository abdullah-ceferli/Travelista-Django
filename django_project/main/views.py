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
# Create your views here.


def index(request):
    user_messages = UserContact.objects.filter(check_box=True).order_by('-id')[:8]
    count = user_messages.count() 

    user_messages_carusel = None
    dot_count = 0

    if count >= 4:
        user_messages_carusel = user_messages
        dot_count = math.ceil(count / 2)

    data = {
        'user_messages_carusel': user_messages_carusel,
        'dot_count': range(dot_count),
    }

    return render(request, 'pages/index.html', data)


def about(request):
    messages = UserMessage.objects.filter(check_box=True).order_by('-id')[:8]
    count = len(messages)

    user_messages_carusel = None
    dot_count = 0

    if count >= 4:
        user_messages_carusel = messages
        dot_count = math.ceil(count / 2)

    data = {
        'user_messages_carusel': user_messages_carusel,
        'dot_count': range(dot_count),
    }
    return render(request, 'pages/about.html', data)


def packages(request):
    destinations_list = Destinations.objects.prefetch_related(
        'destinationsamenity_set__amenity').all()

    data = {'destinations_list': destinations_list, }

    return render(request, 'pages/packages.html', data)


def hotels(request):
    hotel_list = Hotel.objects.prefetch_related(
        'hotelamenity_set__amenity').all()

    data = {'hotel_list': hotel_list, }

    return render(request, 'pages/hotels.html', data)


def blogHome(request):
    return render(request, 'pages/blog-home.html')


def blogSingle(request):
    user_comments = UserMessage.objects.filter(
        check_box=True).order_by('-id')[:10]

    comment_count = user_comments.count()

    show_default = comment_count < 5

    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")
        subject = request.POST.get("subject")
        user_img = request.FILES.get("user_img")

        full_content = f"{name} {email} {message}"

        if not is_message_appropriate(full_content):
            return render(request, 'pages/blog-single.html', {
                "error": "Message blocked! Please do not use inappropriate language.",
                "name": name,
                "email": email,
                "subject": subject,
                "message": message,
                "user_comments": user_comments,
                "show_default": show_default,
            })

        UserMessage.objects.create(
            name=name,
            email=email,
            message=message,
            user_img=user_img,
            subject=subject,
        )

        messages.success(request, "Thank you for your comment!")
        return redirect('index')

    return render(request, 'pages/blog-single.html', {
        'user_comments': user_comments,
        'show_default': show_default,
    })


def contact(request):
    if request.method == "POST":
        name = request.POST.get("name")
        surname = request.POST.get("surname")
        email = request.POST.get("email")
        subject = request.POST.get("subject")
        message = request.POST.get("message")
        user_img = request.FILES.get("user_img")
        stars = request.POST.get("stars", 5)

        full_content = f"{subject} {message}"

        if not is_message_appropriate(full_content):
            return render(request, 'pages/contact.html', {
                "error": "Message blocked! Please do not use inappropriate language.",
                "name": name,
                "surname": surname,
                "email": email,
                "subject": subject,
                "message": message,
            })

        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ipaddress = x_forwarded_for.split(',')[-1].strip()
        else:
            ipaddress = request.META.get('REMOTE_ADDR')

        UserContact.objects.create(
            name=name,
            surname=surname,
            email=email,
            subject=subject,
            message=message,
            user_img=user_img,
            stars=stars,
            ip_address=ipaddress,    
            pub_date=timezone.now()    
        )

        messages.success(request, "Thank you! Your message has been sent.")
        return redirect('index')

    return render(request, 'pages/contact.html')


def elements(request):
    return render(request, 'pages/elements.html')


def insurance(request):
    return render(request, 'pages/insurance.html')

def profile(request):
    return render(request, 'pages/profile.html')


def auth_page(request):
    if request.method == "POST":
        form_type = request.POST.get("form_type")

        if form_type == "signup":
            username = request.POST.get("username")
            email = request.POST.get("email")
            password = request.POST.get("password")
            phone = request.POST.get("phone")

            if SignUp.objects.filter(username=username).exists():
                return render(request, "pages/auth_page.html", {"error": "Username already taken."})

            if SignUp.objects.filter(email=email).exists():
                return render(request, "pages/auth_page.html", {"error": "Email already registered."})

            try:
                email_info = validate_email(email, check_deliverability=True)
                email = email_info.normalized
            except EmailNotValidError as e:
                return render(request, "pages/auth_page.html", {"error": str(e)})

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
                return render(request, "pages/auth_page.html", {"error": "We couldn't send the code. Please check your email address."})

            secure_password = encrypt_password(password)
            request.session['temp_user'] = {
                'username': username,
                'email': email,
                'phone': phone,
                'password': secure_password,
                'code': code
            }
            return redirect('verify_page')

    return render(request, "pages/auth_page.html")


def verify_page(request):
    temp_data = request.session.get('temp_user')

    if not temp_data:
        return redirect('auth_page')

    if request.method == "POST":
        user_code = request.POST.get("code")

        if temp_data['code'] == user_code:
            SignUp.objects.create(
                username=temp_data['username'],
                email=temp_data['email'],
                phone=temp_data['phone'],
                password=temp_data['password']
            )
            del request.session['temp_user']
            return render(request, "pages/auth_page.html", {"success": "Account Verified and Created!"})
        else:
            return render(request, "pages/verify.html", {"error": "Wrong code!"})

    return render(request, "pages/verify.html")