from django.shortcuts import render

# Empty view just rendering the template
def login_view(request):
    return render(request, 'login/login.html')
