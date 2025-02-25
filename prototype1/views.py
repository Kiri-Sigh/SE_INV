from django.shortcuts import render
from django.views import View

class MainPage(View):
    pass
from django.shortcuts import redirect
from social_django.utils import load_strategy

# Empty view just rendering the template
def my_view(request):
    print("Method:", request.method)
    print("Path:", request.path)
    print("Full URL:", request.build_absolute_uri())
    print("User:", request.user if request.user.is_authenticated else "Anonymous")
    print("Query Params:", request.GET)
    print("Body (Raw Data):", request.body)
    print("Cookies:", request.COOKIES)
    print("Headers:", request.headers.get("User-Agent"))
    
    return None

def home_view(request):
    return render(request, 'home/home.html')

def home_view2(request):
    my_view(request)
    print("request",request.session.items())
    return render(request, 'home/home2.html')

# @csrf_extempt
def login_view(request):
    return render(request, 'login/login.html')

# def google_login(request):
#     strategy = load_strategy(request)
#     redirect_uri = strategy.setting("SOCIAL_AUTH_GOOGLE_OAUTH2_REDIRECT_URI")
#     print(f"Redirect URI being used: {redirect_uri}")  # Debugging
#     return redirect("social:begin", backend="google-oauth2")