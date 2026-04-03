from django_user_agents.utils import get_user_agent
from django.shortcuts import redirect, render
from main.models import *
from main.utils import is_message_appropriate
from django.contrib import messages
from django.utils import timezone
import random
from django.core.mail import send_mail
from email_validator import validate_email, EmailNotValidError
from main.utils import encrypt_password
from main.serializers import *
from django.views.generic import ListView, TemplateView, DetailView
from django.db.models import F, Count, Q
# Create your views here.


class HomeView(TemplateView):
    template_name = 'pages/index.html'

    def get(self, request, *args, **kwargs):
        user_id = request.session.get('user_id')
        if not user_id:
            return redirect('auth_page')

        user_data = SignUp.objects.filter(id=user_id).first()
        if user_data and not user_data.name:
            return redirect('setup_profile')

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.request.session.get('user_id')
        context['current_user'] = SignUp.objects.filter(id=user_id).first()
        context['recent_posts'] = BlogPost.objects.all().order_by('-pub_date')[:4]
        
        return context


class AboutView(TemplateView):
    template_name = 'pages/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        items = UserContact.objects.filter(
            check_box=True).order_by('-pub_date')[:8]
        count = items.count()
        num_dots = (count // 2) + 1 if count > 0 else 0

        context['carousel_items'] = items
        context['dots_range'] = range(num_dots)

        return context


class PackagesView(TemplateView):
    template_name = 'pages/packages.html'


class HotelsView(TemplateView):
    template_name = 'pages/hotels.html'


class BlogHomeView(ListView): 
    model = BlogPost
    template_name = 'pages/blog-home.html'
    context_object_name = 'posts'  
    paginate_by = 4 

    def get_queryset(self):
        queryset = BlogPost.objects.annotate(
            total_comments=Count('comments') 
        ).order_by('-pub_date')
        
        query = self.request.GET.get('q')
        
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) | 
                Q(content__icontains=query)
            ).distinct()
            
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['categories'] = Tag.objects.annotate(
            post_count=Count('blog_posts')
        ).order_by('name')

        context['tags'] = Tag.objects.all()
        context['popular_posts'] = BlogPost.objects.all().order_by('-view_count')[:4]
        context['search_query'] = self.request.GET.get('q')

        user_id = self.request.session.get('user_id')
        if user_id:
            context['logged_in_user'] = SignUp.objects.filter(id=user_id).first()
        
        return context


class BlogSingleView(DetailView):
    model = BlogPost
    template_name = 'pages/blog-single.html'
    context_object_name = 'post'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        session_key = f'viewed_post_{self.object.pk}'
        if not request.session.get(session_key, False):
            BlogPost.objects.filter(pk=self.object.pk).update(view_count=F('view_count') + 1)
            request.session[session_key] = True
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        all_msgs = UserMessage.objects.filter(blog_post=self.object)
        approved_msgs = all_msgs.filter(check_box=True)
        
        context['comments'] = approved_msgs.order_by('-pub_date')
        context['comment_count'] = approved_msgs.count()

        user_id = self.request.session.get('user_id')
        if user_id:
            context['logged_in_user'] = SignUp.objects.filter(id=user_id).first()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object() 
        user_id = request.session.get('user_id')
        user = SignUp.objects.filter(id=user_id).first()
        
        message_text = request.POST.get("message", "")
        
        is_safe = is_message_appropriate(message_text)

        UserMessage.objects.create(
            blog_post=self.object, 
            user_profile=user,
            name=f"{user.name} {user.last_name}" if user else request.POST.get("name"),
            email=user.email if user else request.POST.get("email"),
            subject=request.POST.get("subject", ""),
            message=message_text,
            check_box=is_safe,  
            user_img=user.profile_img if user and user.profile_img else None 
        )
        
        return redirect('blog-single', pk=self.object.pk)


class ContactView(TemplateView):
    template_name = 'pages/contact.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        name = request.POST.get("name")
        surname = request.POST.get("surname")
        email = request.POST.get("email")
        subject = request.POST.get("subject")
        message = request.POST.get("message")
        stars = request.POST.get("stars", 5)

        user_id = request.session.get('user_id')
        final_img = None

        if user_id:
            user_profile = SignUp.objects.filter(id=user_id).first()
            if user_profile and user_profile.profile_img:
                final_img = user_profile.profile_img

        full_content = f"{subject} {message}"
        if not is_message_appropriate(full_content):
            return render(request, self.template_name, {
                "error": "Message blocked! Inappropriate language.",
                "name": name, "surname": surname, "email": email,
                "subject": subject, "message": message,
            })

        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        ip_address = x_forwarded_for.split(
            ',')[-1].strip() if x_forwarded_for else request.META.get('REMOTE_ADDR')

        UserContact.objects.create(
            name=name,
            surname=surname,
            email=email,
            subject=subject,
            message=message,
            user_img=final_img,
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

    def get(self, request, *args, **kwargs):
        user_id = request.session.get('user_id')

        if not user_id:
            return redirect('auth_page')

        user_data = SignUp.objects.filter(id=user_id).first()

        if not user_data:
            return redirect('auth_page')

        if not user_data.name:
            return redirect('setup_profile')

        context = self.get_context_data(**kwargs)
        context['profile_user'] = user_data
        context['logged_in_user'] = user_data 
        user_posts = BlogPost.objects.filter(author=user_data)
        context['post_count'] = user_posts.count()
        context['photo_count'] = user_posts.exclude(blog_img="").exclude(blog_img__isnull=True).count()

        try:
            comment_queryset = user_data.messages.all()
        except AttributeError:
            comment_queryset = user_data.usermessage_set.all()

        context['comment_count'] = comment_queryset.count()
        context['comments'] = comment_queryset.select_related('blog_post').order_by('-pub_date')

        return self.render_to_response(context)


class AuthView(TemplateView):
    template_name = "pages/auth_page.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        form_type = request.POST.get("form_type")
        if form_type == "signup":
            return self.handle_signup(request)
        elif form_type == "login":
            return self.handle_login(request)
        return render(request, self.template_name)

    def handle_login(self, request):
        email = request.POST.get("email")
        password = request.POST.get("password")
        encrypted_attempt = encrypt_password(password)
        user = SignUp.objects.filter(
            email=email, password=encrypted_attempt).first()

        if user:
            request.session['user_id'] = user.id
            request.session['username'] = user.username
            request.session.set_expiry(1209600)
            return redirect('index')
        else:
            return render(request, self.template_name, {
                "error": "Invalid email or password.",
                "form_type": "login"
            })

    def handle_signup(self, request):
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        phone = request.POST.get("phone")

        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        ip_address = x_forwarded_for.split(
            ',')[0] if x_forwarded_for else request.META.get('REMOTE_ADDR')

        user_agent = get_user_agent(request)
        if user_agent.is_mobile:
            device = "Mobile"
        elif user_agent.is_pc:
            device = "PC"
        elif user_agent.is_tablet:
            device = "Tablet"
        else:
            device = "Bot/Unknown"

        os_family = user_agent.os.family
        os_version = user_agent.os.version_string
        browser_family = user_agent.browser.family
        browser_version = user_agent.browser.version_string

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
                    <h2 style="color: #2d3436;">Verify Your Account</h2>
                    <div style="font-size: 36px; font-weight: bold; color: #0984e3; background: #f1f2f6; padding: 15px; border-radius: 8px; letter-spacing: 6px; margin: 25px 0;">
                        {code}
                    </div>
                </div>
            </div>
        """

        try:
            print(f"\nSending email to {email} with code {code}\n")
            send_mail(
                'Your Verification Code',
                f"Your code is: {code}",
                'speedwagerreal2@gmail.com',
                [email],
                fail_silently=False,
                html_message=html_content,
            )
        except Exception:
            return render(request, self.template_name, {"error": "Failed to send email."})

        request.session['temp_user'] = {
            'username': username,
            'email': email,
            'phone': phone,
            'password': encrypt_password(password),
            'code': code,
            'ip_address': ip_address,
            'device_type': device,
            'os_family': os_family,
            'os_version': os_version,
            'browser_family': browser_family,
            'browser_version': browser_version
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
            user = SignUp.objects.create(
                username=temp_data['username'],
                email=temp_data['email'],
                phone=temp_data['phone'],
                password=temp_data['password'],
                ip_address=temp_data.get('ip_address'),
                device_type=temp_data.get('device_type'),
                os_family=temp_data.get('os_family'),
                os_version=temp_data.get('os_version'),
                browser_family=temp_data.get('browser_family'),
                browser_version=temp_data.get('browser_version')
            )

            request.session['user_id'] = user.id
            request.session['username'] = user.username
            request.session.set_expiry(1209600)

            del request.session['temp_user']

            return redirect('setup_profile')
        else:
            return render(request, self.template_name, {"error": "Invalid code."})


class LogoutView(TemplateView):
    def get(self, request):
        request.session.flush()
        return redirect('auth_page')


class SetupProfileView(TemplateView):
    template_name = "pages/setup_profile.html"

    def get(self, request, *args, **kwargs):
        if not request.session.get('user_id'):
            return redirect('auth_page')
        return self.render_to_response({})

    def post(self, request, *args, **kwargs):
        user_id = request.session.get('user_id')
        user = SignUp.objects.filter(id=user_id).first()

        if not user:
            return redirect('auth_page')

        name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        age = request.POST.get("age")
        location = request.POST.get("location")
        profile_img = request.FILES.get("profile_img")

        if not all([name, last_name, age, location]):
            return render(request, self.template_name, {
                "error": "Please fill in all required fields.",
            })

        user.name = name
        user.last_name = last_name
        user.age = age
        user.location = location
        user.about_me = request.POST.get("about_me", "")
        user.contact_email = request.POST.get("contact_email", "")

        if profile_img:
            user.profile_img = profile_img

        user.save()

        return redirect('profile')


class AddBlogView(TemplateView):
    template_name = 'pages/add-blog.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.get_common_context())

    def post(self, request, *args, **kwargs):
        title = request.POST.get('title')
        content = request.POST.get('content')
        new_tag_name = request.POST.get('new_tag', '').strip()
        
        selected_tag_ids = request.POST.getlist('tags') 

        if new_tag_name and not is_message_appropriate(new_tag_name):
            messages.error(request, f"The tag '{new_tag_name}' is inappropriate.")
            context = self.get_common_context()
            context.update({
                'typed_title': title,
                'typed_content': content,
                'selected_tags': [int(i) for i in selected_tag_ids] 
            })
            return render(request, self.template_name, context)

        user_id = request.session.get('user_id')
        author = SignUp.objects.filter(id=user_id).first() if user_id else None
        
        blog = BlogPost.objects.create(
            title=title,
            content=content,
            author=author,
            blog_img=request.FILES.get('blog_img')
        )

        if selected_tag_ids:
            blog.tags.add(*selected_tag_ids)

        if new_tag_name:
            tag_obj, _ = Tag.objects.get_or_create(name=new_tag_name)
            blog.tags.add(tag_obj)

        messages.success(request, "Blog posted successfully!")
        return redirect('blog-home')

    def get_common_context(self):
        context = {
            'tags': Tag.objects.all(),
            'selected_tags': [], 
        }
        user_id = self.request.session.get('user_id')
        if user_id:
            context['logged_in_user'] = SignUp.objects.filter(id=user_id).first()
        return context


class CategoryDetailView(ListView):
    model = BlogPost
    template_name = 'pages/blog-home.html'
    context_object_name = 'posts'
    paginate_by = 4

    def get_queryset(self):
        return BlogPost.objects.filter(tags__id=self.kwargs['tag_id']).order_by('-pub_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['categories'] = Tag.objects.annotate(
            post_count=Count('blog_posts')
        ).order_by('name')

        context['tags'] = Tag.objects.all()

        user_id = self.request.session.get('user_id')
        if user_id:
            context['logged_in_user'] = SignUp.objects.filter(id=user_id).first()
            
        return context


class ConnectsView(TemplateView):
    template_name = 'pages/connect.html'
