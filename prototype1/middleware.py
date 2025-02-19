from django.contrib.auth import login
from django.utils.deprecation import MiddlewareMixin
from user.models import CustomUser  # Import your user model


#ok
class AutoLoginMiddleware(MiddlewareMixin):
    def process_request(self, request):
        #print("process req run")
        print("req session",request.session.items())

        if not request.user.is_authenticated:
            google_id = request.session.get("google_id")  # Retrieve Google ID from session
            if google_id:
                user = CustomUser.objects.filter(google_id=google_id).first()
                if user:
                    print("logged in")
                    login(request, user)
