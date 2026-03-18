from django.shortcuts import redirect, render
from main.models import *
from main.utils import is_message_appropriate
from django.contrib import messages
from ipware import get_client_ip
# Create your views here.


def about(request):
    return render(request, 'pages/about.html')


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
            user_ip=client_ip
        )

        messages.success(request, "Thank you! Your message has been sent.")
        return redirect('index')

    return render(request, 'pages/contact.html')


def elements(request):
    return render(request, 'pages/elements.html')


def hotels(request):
    return render(request, 'pages/hotels.html')


def index(request):

    return render(request, 'pages/index.html')


def insurance(request):
    return render(request, 'pages/insurance.html')


def packages(request):
    return render(request, 'pages/packages.html')
