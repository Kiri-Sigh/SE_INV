from django.shortcuts import render

# Empty view just rendering the template
def home_view(request):
    return render(request, 'home/home.html')

def login_view(request):
    return render(request, 'login/login.html')
from django.shortcuts import redirect
from social_django.utils import load_strategy

# def google_login(request):
#     strategy = load_strategy(request)
#     redirect_uri = strategy.setting("SOCIAL_AUTH_GOOGLE_OAUTH2_REDIRECT_URI")
#     print(f"Redirect URI being used: {redirect_uri}")  # Debugging
#     return redirect("social:begin", backend="google-oauth2")