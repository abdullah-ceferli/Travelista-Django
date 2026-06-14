{% load static %}
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Travel</title>
    <link rel="stylesheet" href="{% static 'css/own-bootstrap.css' %}">
    <link rel="stylesheet" href="{% static 'css/add-blog.css' %}">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
    <link rel="stylesheet" href="https://cdn.linearicons.com/free/1.0.0/icon-font.min.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
</head>

<body>
    <div id="site-preloader">
        <div class="loader-content">
            <div class="dot"></div>
            <div class="dot"></div>
            <div class="dot"></div>
            <p>Preparing your journey...</p>
        </div>
    </div>
    <div class="wrapper">
        <header class="header banner-area">
            <nav class="nav-bar" id="nav-bar">
                <div class="nav-bar-top">
                    <div class="container">
                        <div class="nav-bar-top-scrolling">
                            <div class="nav-bar-top-left">
                                <ul>
                                    <li><a href="#">Visit Us</a></li>
                                    <li><a href="#">Buy Tickets</a></li>
                                </ul>
                            </div>
                            <div class="nav-bar-top-right">
                                <div class="nav-bar-social">
                                    <a href="#"><i class="fa-brands fa-facebook"></i></a>
                                    <a href="#"><i class="fa-brands fa-x-twitter"></i></a>
                                    <a href="#"><i class="fa-brands fa-dribbble"></i></a>
                                    <a href="#"><i class="fa-brands fa-behance"></i></a>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="container nav-bar-main-menu">
                    <button type="button" id="mobile-nav-toggle"><i class="lnr lnr-menu"></i></button>
                    <div class="nav-bar-main-menu-full">
                        <div id="logo">
                            <a href="{% url 'index' %}"><img src="{% static 'img/logo.png' %}" alt="" title=""></a>
                        </div>
                        <nav id="nav-menu-container">
                            <ul class="nav-menu sf-js-enabled sf-arrows" style="touch-action: pan-y;">
                                <li><a href="{% url 'index' %}" class="menu-active">Home</a></li>
                                <li><a href="{% url 'about' %}">About</a></li>
                                <li><a href="{% url 'packages' %}">Packages</a></li>
                                <li><a href="{% url 'hotels' %}">Hotels</a></li>
                                <li><a href="{% url 'insurance' %}">Insurance</a></li>
                                <li class="menu-has-children"><a href="{% url 'profile' %}"
                                        class="sf-with-ul">Profile</a>
                                    <ul>
                                        <li><a href="{% url 'profile' %}">Profile</a></li>
                                        <li><a href="{% url 'auth_page' %}">Auth Page</a></li>
                                    </ul>
                                </li>
                                <li class="menu-has-children"><a href="{% url 'blog-home' %}"
                                        class="sf-with-ul">Blog</a>
                                    <ul>
                                        <li><a href="{% url 'blog-home' %}">Blog Home</a></li>
                                        <li><a href="{% url 'add_blog' %}">Add Blog</a></li>
                                    </ul>
                                </li>
                                <li class="menu-has-children"><a href="{% url 'elements' %}"
                                        class="sf-with-ul">Pages</a>
                                    <ul>
                                        <li><a href="{% url 'elements' %}">Elements</a></li>
                                        <li class="menu-has-children"><a href="" class="sf-with-ul">Level 2 </a>
                                            <ul>
                                                <li><a href="#">Item One</a></li>
                                                <li><a href="#">Item Two</a></li>
                                            </ul>
                                        </li>
                                    </ul>
                                </li>
                                <li><a href="{% url 'contact' %}">Contact</a></li>
                            </ul>
                        </nav>
                    </div>
                </div>
            </nav>
            <div class="overlay overlay-bg"></div>
            <div class="hero-section" style="height: 340px;">
                <div class="container">
                    <div class="hero-section-main">
                        <div class="hero-section-title">
                            <h1>
                                Blog Details Page
                            </h1>
                            <p class="text-white link-nav"><a href="{% url 'index' %}">Home </a> <i
                                    class="fa-solid fa-arrow-right"></i> <a href="{% url 'add_blog' %}"> Add Blog </a>
                            </p>
                        </div>
                    </div>
                </div>

            </div>
        </header>
        <main class="main">
            <!-- Start Post Content Section -->
            <section class="post-content-section">
                <div class="container">
                    <div class="add-blog-container">
                        <div class="blog-card">
                            <div class="blog-card-header">
                                <h3>Create New Post</h3>
                            </div>

                            <form action="" method="POST" enctype="multipart/form-data" class="blog-form">
                                {% csrf_token %}

                                <div class="post-user-info">
                                    <div class="user-avatar">
                                        <img src="{% if logged_in_user %}{{ logged_in_user.profile_img.url }}{% else %}/static/img/user-img/user-info.png{% endif %}"
                                            alt="">
                                    </div>
                                    <div class="user-meta">
                                        <span class="user-name">{% if logged_in_user %}{{ logged_in_user.name }}{% else %}Guest User{% endif %}</span>
                                    </div>
                                </div>

                                <div class="input-group">
                                    <input type="text" name="title" value="{{ typed_title|default:'' }}"
                                        placeholder="Title..." required>
                                </div>

                                <div class="input-group">
                                    <label class="input-label">Categories (Select 2-3 tags)</label>
                                    <select name="tags" class="custom-select" multiple style="height: 120px;">
                                        {% for tag in tags %}
                                        <option value="{{ tag.id }}" {% if tag.id in selected_tags %}selected{% endif %}>
                                            {{ tag.name }}
                                        </option>
                                        {% endfor %}
                                    </select>
                                    <small style="color: #65676b;">Hold Ctrl (Cmd on Mac) to select more than
                                        one.</small>
                                    <input type="text" name="new_tag" class="mt-10"
                                        placeholder="Or create a new tag...">
                                </div>

                                <div class="input-group">
                                    <textarea name="content" rows="6" placeholder="What's on your mind?"
                                        required>{{ typed_content|default:'' }}</textarea>
                                </div>

                                <div class="file-upload-wrapper">
                                    <label for="blog_img" class="file-label"><i class="fa fa-image"></i> Add
                                        Image</label>
                                    <input type="file" name="blog_img" id="blog_img">
                                </div>

                                <button type="submit" class="submit-btn">Publish Post</button>
                            </form>

                            {% if messages %}
                            <div class="message-container">
                                {% for message in messages %}
                                <div class="custom-alert alert-{{ message.tags }}">
                                    <i class="fa {% if message.tags == 'error' or message.tags == 'danger' %}fa-exclamation-circle{% else %}fa-check-circle{% endif %}"
                                        style="margin-right: 10px;"></i>
                                    {{ message }}
                                </div>
                                {% endfor %}
                            </div>
                            {% endif %}
                        </div>
                    </div>
                </div>
            </section>
            <!-- End Post Content Section -->
        </main>
        <footer class="footer section-gap">
            <div class="container">
                <div class="footer-top">
                    <div class="footer-top-sections">
                        <div class="footer-top-sections-widget">
                            <h6>About Agency</h6>
                            <p>
                                The world has become so fast paced that people don’t want to stand by reading a page of
                                information, they would much rather look at a presentation and understand the message.
                                It has come to a point
                            </p>
                        </div>
                    </div>
                    <div class="footer-top-sections">
                        <div class="footer-top-sections-widget">
                            <h6>Navigation Links</h6>
                            <div class="row">
                                <div class="col">
                                    <ul>
                                        <li><a href="{% url 'index' %}">Home</a></li>
                                        <li><a href="#">Feature</a></li>
                                        <li><a href="#">Services</a></li>
                                        <li><a href="#">Portfolio</a></li>
                                    </ul>
                                </div>
                                <div class="col">
                                    <ul>
                                        <li><a href="#">Team</a></li>
                                        <li><a href="#">Pricing</a></li>
                                        <li><a href="{% url 'blog-home' %}">Blog</a></li>
                                        <li><a href="{% url 'contact' %}">Contact</a></li>
                                    </ul>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="footer-top-sections">
                        <div class="single-footer-widget">
                            <h6>Newsletter</h6>
                            <p>
                                For business professionals caught between high OEM price and mediocre print and graphic
                                output.
                            </p>
                            <div>
                                <form method="get" class="subscription" novalidate="true">
                                    <div class="footer-top-input">
                                        <input name="EMAIL" placeholder="Email Address" onfocus="this.placeholder = ''"
                                            onblur="this.placeholder = 'Email Address '" required="" type="email">

                                        <button class="footer-top-button"><i
                                                class="fa-regular fa-paper-plane"></i></button>
                                    </div>

                                    <!-- can put animate here -->
                                </form>
                            </div>
                        </div>
                    </div>
                    <div class="footer-top-sections">
                        <div class="single-footer-widget">
                            <h6 class="mb-20">InstaFeed</h6>
                            <ul class="footer-top-img">
                                <li><img src="{% static 'img/footer-img/i1.jpg' %}" alt=""></li>
                                <li><img src="{% static 'img/footer-img/i2.jpg' %}" alt=""></li>
                                <li><img src="{% static 'img/footer-img/i3.jpg' %}" alt=""></li>
                                <li><img src="{% static 'img/footer-img/i4.jpg' %}" alt=""></li>
                                <li><img src="{% static 'img/footer-img/i5.jpg' %}" alt=""></li>
                                <li><img src="{% static 'img/footer-img/i6.jpg' %}" alt=""></li>
                                <li><img src="{% static 'img/footer-img/i7.jpg' %}" alt="">
                                <li><img src="{% static 'img/footer-img/i8.jpg' %}" alt=""></li>
                            </ul>
                        </div>
                    </div>
                </div>
                <div class="footer-bottom">
                    <p class="footer-bottom-txt">Copyright ©
                        <script>document.write(new Date().getFullYear());</script> All rights reserved | This template
                        is made with <i class="fa-regular fa-heart"></i> by <a href="#">Colorlib</a>
                    </p>
                    <div class="footer-social">
                        <a href="#"><i class="fa-brands fa-facebook"></i></a>
                        <a href="#"><i class="fa-brands fa-x-twitter"></i></a>
                        <a href="#"><i class="fa-brands fa-dribbble"></i></a>
                        <a href="#"><i class="fa-brands fa-behance"></i></a>
                    </div>
                </div>
            </div>
        </footer>
    </div>
    <script src="{% static 'js/add-blog.js' %}"></script>
    <script>
        function lazyLoad() {
            const preloader = document.getElementById('site-preloader')

            if (!preloader) return

            setTimeout(() => {
                preloader.style.opacity = '0'
                setTimeout(() => {
                    preloader.style.display = 'none'
                }, 500)
            }, 200)
        }

        window.addEventListener('DOMContentLoaded', () => {
            navBarLinksChilds()
            navBarMovement()
            smoothUp()


            lazyLoad()
        })
    </script>
</body>

</html>