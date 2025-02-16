from user.models import CustomUser

def set_student_defaults(strategy, details, backend, user=None, *args, **kwargs):
    """ Ensure new users have required fields """
    if user and isinstance(user, CustomUser):  # Check if user exists & is correct type
        user.enrolled_year = 2024
        user.merit = 0
        user.save()
    return {'user': user}
# def save_google_profile(backend, user, response, *args, **kwargs):
#     """
#     Save additional data from Google's API to the user profile.
#     """
#     if backend.name == "google-oauth2":
#         if user.social_auth.filter(provider=backend.name).exists():
#             user.google_id = response.get("sub")  # Save Google ID
#             user.profile_picture = response.get("picture")  # Save profile picture
#             user.save()
#         else:
#             # Optionally create a profile if one doesn't exist
#             user.google_id = response.get("sub")  # Save Google ID
#             user.profile_picture = response.get("picture")  # Save profile picture
#             user.save()

# user/pipeline.py


def save_google_profile(backend, user, response, *args, **kwargs):
    if backend.name == 'google':
        # Ensure that the user is associated with a CustomUser instance
        custom_user, created = CustomUser.objects.get_or_create(
            user=user,  # Associate it with the `auth_user` model
            defaults={
                'profile_picture': response.get('picture', None),
            }
        )
        if not created:
            # If the CustomUser already exists, update additional information if needed
            custom_user.profile_picture = response.get('picture', None)
            custom_user.save()

from django.contrib.auth import get_user_model
from social_core.exceptions import AuthAlreadyAssociated
from social_django.models import UserSocialAuth

User = get_user_model()

def allow_reassociation(backend, user, *args, **kwargs):
    from social_core.exceptions import AuthAlreadyAssociated
    
    
    if not user:
        email = kwargs.get('details', {}).get('email')
        if email:
            try:
                # Find existing user by email
                user = get_user_model().objects.get(email=email)
                existing_social_user = UserSocialAuth.objects.filter(user=user, provider=backend.name).exists()
                if existing_social_user:
                    return {'user': user}
                else:
                    raise AuthAlreadyAssociated(backend)
            except get_user_model().DoesNotExist:
                pass
    return None


def auto_login_existing_user(backend, uid, user=None, response=None, *args, **kwargs):
    """
    If a user tries to log in with a social account that already exists, log them in.
    """
    if user:  # User is already authenticated, no need to check
        return {"user": user}

    social_auth = UserSocialAuth.objects.filter(provider=backend.name, uid=uid).first()

    if social_auth:
        return {"user": social_auth.user}  # Log in the existing user

    # If no social auth exists, check if there's a user with the same email
    email = kwargs.get("details", {}).get("email")
    if email:
        try:
            existing_user = User.objects.get(email=email)
            return {"user": existing_user}  # Log in the user with the existing email
        except User.DoesNotExist:
            pass

    return None  # Continue with default pipeline (creating new user if necessary)


from social_core.exceptions import AuthException

def print_google_response(backend, user, response, *args, **kwargs):
    """
    This function prints the response data received from Google
    when a user logs in via Google OAuth2.
    """
    # Check if the backend is Google OAuth2
    if backend.name == 'google':
        # Print the response data
        print("Google response data:", response)
    return None