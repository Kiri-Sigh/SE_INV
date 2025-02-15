from social_django.models import UserSocialAuth

def get_google_profile(user):
    try:
        social = user.social_auth.get(provider='google-oauth2')  # Get social auth object
        return social.extra_data  # Returns JSON data (name, email, etc.)
    except UserSocialAuth.DoesNotExist:
        return None
