from django.shortcuts import redirect

class ProfileCompletionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        allowed_paths = ['/pages/setup_profile/', '/logout/', '/api/']
        
        user_id = request.session.get('user_id')
        
        if user_id and not any(request.path.startswith(p) for p in allowed_paths):
            from .models import SignUp
            user = SignUp.objects.filter(id=user_id).first()
            if user and not user.name:
                return redirect('setup_profile')

        return self.get_response(request)