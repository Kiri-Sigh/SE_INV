# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from social_django.models import UserSocialAuth
from .utils import get_google_profile


@login_required  # Ensure only logged-in users can access
def social_profile(request):
    user = request.user
    try:
        google_data = get_google_profile(user)
    except:
        google_data = None
    return render(request, "users/social_profile.html", {"google_data": google_data})
# from django.shortcuts import redirect
# from social_django.utils import load_strategy

# def google_login(request):
#     strategy = load_strategy(request)
#     redirect_uri = strategy.setting("SOCIAL_AUTH_GOOGLE_OAUTH2_REDIRECT_URI")
#     print(f"Redirect URI being used: {redirect_uri}")  # Debugging
#     return redirect("social:begin", backend="google-oauth2")
from django.shortcuts import render
from .utils import get_google_user_data  # Import the function

def profile_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    try:
        google_data = get_google_user_data(request.user)
    except:
        google_data = None
    return render(request, 'profile.html', {'google_data': google_data}
