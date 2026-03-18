# py .\django_project\manage.py runserver
# host - http://127.0.0.1:8000/

password - 1234 
user_Name - admin
email - abdullahdj234@gmail.com
You can run yourself for try


# py .\django_project\manage.py runserver 0.0.0.0:8001
# cloudflared tunnel --url http://localhost:8001




# powershell commands for this django project
# 1. media img cleaner
+ python .\django_project\manage.py cleanup_media

- creats new bin/project_img
- and put not using img from media which not using in dataBase

# 2. bin img cleaner 
+ python .\django_project\manage.py cleanup_bin

- delets bin/project_img/img 

# or can use second variant
+ python .\django_project\manage.py cleanup_bin --force

- do some thing but not seying to u "Are you sure"