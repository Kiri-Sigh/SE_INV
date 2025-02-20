from django.contrib.auth import login
from django.utils.deprecation import MiddlewareMixin
from user.models import CustomUser  # Import your user model
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed


#ok
class AutoLoginMiddleware(MiddlewareMixin):
    def process_request(self, request):
        #print("process req run")
        #print("req session",request.session.items())

        if not request.user.is_authenticated:
            google_id = request.session.get("google_id")  # Retrieve Google ID from session
            if google_id:
                user = CustomUser.objects.filter(google_id=google_id).first()
                if user:
                    print("logged in")
                    login(request, user)


class JWTAuthMiddleware2:
    def __init__(self, get_response):
        print(get_response)
        self.get_response = get_response

    def __call__(self, request):
        try:
            # Attempt to authenticate using the JWT token in cookies
            print("doing this")
            auth = JWTAuthentication()
            auth_result = auth.authenticate(request)
            
            if auth_result is not None:
                user, auth_token = auth_result
                request.user = user
                print("middleware auth yes")
            else:
                print("middleware auth no token found")
                request.user = None
        except AuthenticationFailed:
            print("middleware auth no")
            request.user = None
        return self.get_response(request)
    
class JWTAuthMiddleware:
    def __init__(self, get_response):
        print(get_response)
        self.get_response = get_response

    def __call__(self, request):
        try:
            # Attempt to authenticate using the JWT token in cookies
            print("doing this")
            print("1",JWTAuthentication())
            print("2",JWTAuthentication().authenticate(request))
            auth = JWTAuthentication()
            user, auth_token = auth.authenticate(request)
            if user:
                request.user = user
                print("middleware auth yes")
            else:
                print("No user found")
        except AuthenticationFailed:
            print("middleware auth no")
            request.user = None
        except Exception as e:
            print(f"Error during authentication: {e}")
            request.user = None
        return self.get_response(request)

