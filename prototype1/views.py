from django.shortcuts import render

# Empty view just rendering the template
def home_view(request):
    return render(request, 'home/home.html')

def login_view(request):
    return render(request, 'login/login.html')
