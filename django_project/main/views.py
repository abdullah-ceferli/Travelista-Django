from django.shortcuts import redirect, render
from main.models import *
from main.utils import is_message_appropriate
from django.contrib import messages
from ipware import get_client_ip
import math
# Create your views here.


def index(request):
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

    
    return render(request, 'pages/blog-single.html')


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

        client_ip, is_routable = get_client_ip(request)

        UserMessage.objects.create(
            name=name,
            surname=surname,
            email=email,
            subject=subject,
            message=message,
            user_img=user_img,
            user_ip=client_ip,
            stars=stars,
        )

        messages.success(request, "Thank you! Your message has been sent.")
        return redirect('index')

    return render(request, 'pages/contact.html')


def elements(request):
    return render(request, 'pages/elements.html')


def insurance(request):
    return render(request, 'pages/insurance.html')
