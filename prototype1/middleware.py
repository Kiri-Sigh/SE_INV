from django.contrib.auth import login
from django.utils.deprecation import MiddlewareMixin
from user.models import CustomUser  # Import your user model
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed


#ok
class AutoLoginMiddleware(MiddlewareMixin):
    def process_request(self, request):
        #print("process req run")
        print("req session",request.session.items())
        print("req user",request.user)
        if not request.user.is_authenticated:
            google_id = request.session.get("google_id")  # Retrieve Google ID from session
            if google_id:
                user = CustomUser.objects.filter(google_id=google_id).first()
                if user:
                    print("logged in")
                    login(request, user)


class JWTAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            # Extract token from cookies (or any other source) and add it to Authorization header
            access_token = request.COOKIES.get('access_token')  # Assuming token is in cookies
            if access_token:
                request.headers['Authorization'] = f'Bearer {access_token}'
            
            # Proceed with the authentication
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
import requests
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed

class JWTAuthMiddleware2:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            # Retrieve tokens from cookies
            access_token = request.COOKIES.get('access_token')
            refresh_token = request.COOKIES.get('refresh_token')
            
            if access_token:
                # Check if the access token is expired
                if self.is_token_expired(access_token):
                    print("Access token expired. Trying to refresh it.")
                    # If expired, refresh the token using the refresh token
                    new_access_token = self.refresh_access_token(refresh_token)
                    
                    if new_access_token:
                        # Update the access token in the request header
                        request.headers['Authorization'] = f'Bearer {new_access_token}'
                    else:
                        raise AuthenticationFailed("Unable to refresh access token.")
                else:
                    # If access token is not expired, set it in the header
                    request.headers['Authorization'] = f'Bearer {access_token}'
                
                # Proceed with the authentication
                auth = JWTAuthentication()
                user, auth_token = auth.authenticate(request)
                
                if user:
                    request.user = user
                    print("middleware auth yes")
                else:
                    print("No user found")
            else:
                print("No access token found.")
        except AuthenticationFailed:
            print("middleware auth no")
            request.user = None
        except Exception as e:
            print(f"Error during authentication: {e}")
            request.user = None

        return self.get_response(request)

    def is_token_expired(self, token):
        """
        Helper function to check if the JWT access token is expired.
        You can decode the token and check the `exp` field for expiration.
        """
        try:
            import jwt
            decoded_token = jwt.decode(token, options={"verify_signature": False})
            exp_timestamp = decoded_token.get("exp")
            return exp_timestamp < time.time()  # Check if expired
        except Exception as e:
            print(f"Error decoding token: {e}")
            return False

    def refresh_access_token(self, refresh_token):
        """
        Function to refresh the access token using the refresh token.
        It makes a request to the authorization server to obtain a new access token.
        """
        refresh_url = 'https://your-oauth2-server.com/token'  # Replace with your OAuth2 token URL
        refresh_data = {
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token,
            'client_id': 'your-client-id',  # Replace with your client ID
            'client_secret': 'your-client-secret'  # Replace with your client secret
        }
        
        # Send request to refresh the access token
        response = requests.post(refresh_url, data=refresh_data)
        
        if response.status_code == 200:
            new_tokens = response.json()
            return new_tokens.get('access_token')
        else:
            print("Failed to refresh access token:", response.status_code, response.text)
            return None
