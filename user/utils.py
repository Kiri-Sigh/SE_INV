from social_django.models import UserSocialAuth

def get_google_profile(user):
    try:
        social = user.social_auth.get(provider='google-oauth2')  # Get social auth object
        return social.extra_data  # Returns JSON data (name, email, etc.)
    except UserSocialAuth.DoesNotExist:
        return None
from social_django.utils import load_strategy

def get_google_user_data(user):
    strategy = load_strategy()
    social = user.social_auth.get(provider='google-oauth2')
    
    # Get user info from Google
    extra_data = social.extra_data
    return {
        "id": extra_data.get("id"),
        "email": extra_data.get("email"),
        "name": extra_data.get("name"),
        "picture": extra_data.get("picture"),
        "locale": extra_data.get("locale"),
    }
