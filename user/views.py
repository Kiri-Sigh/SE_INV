
# Create your views here.
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from social_django.models import UserSocialAuth
from .utils import get_google_profile  # Import the function

@login_required  # Ensure only logged-in users can access
def social_profile(request):
    user = request.user
    google_data = get_google_profile(user)  # Get Google OAuth data

    return render(request, "users/social_profile.html", {"google_data": google_data})
# from django.shortcuts import redirect
# from social_django.utils import load_strategy

# def google_login(request):
#     strategy = load_strategy(request)
#     redirect_uri = strategy.setting("SOCIAL_AUTH_GOOGLE_OAUTH2_REDIRECT_URI")
#     print(f"Redirect URI being used: {redirect_uri}")  # Debugging
#     return redirect("social:begin", backend="google-oauth2")
