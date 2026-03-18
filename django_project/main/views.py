from django.shortcuts import redirect, render
from main.models import *
from main.utils import is_message_appropriate
from django.contrib import messages
# Create your views here.


def about(request):
    return render(request, 'pages/about.html')


def blogHome(request):
    return render(request, 'pages/blog-home.html')


def blogSingle(request):
    return render(request, 'pages/blog-single.html')


def contact(request):
    contact_info = ContactInfo.objects.first()

    if request.method == "POST":
        name = request.POST.get("name")
        surname = request.POST.get("surname")
        email = request.POST.get("email")
        subject = request.POST.get("subject")
        message = request.POST.get("message")

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

        UserMessage.objects.create(
            name=name,
            surname=surname,
            email=email,
            subject=subject,
            message=message
        )

        messages.success(request, "Thank you! Your message has been sent.")
        return redirect('index')

    return render(request, 'pages/contact.html', {
        "contact_info": contact_info
    })


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
