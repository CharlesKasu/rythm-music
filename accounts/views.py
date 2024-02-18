import json

from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .forms import RegistrationForm

@csrf_exempt
def register_user(request):
    if request.method == 'POST':
        print("Raw data received:", request.body)

        data = json.loads(request.body)
        print("data",data)
        form = RegistrationForm(data)
        if form.is_valid():
            form.save()
            return JsonResponse({"status": True, "message": "Registration confirmed"})
        else:
            errors = [error for field in form for error in field.errors]
            return JsonResponse({"status": False, "errors": errors})
    else:
        return JsonResponse({"message": "Denied"}, status=400)

@csrf_exempt
def login_user(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        password = data.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return JsonResponse({"status": True, "message": "User logged in"})
            else:
                return JsonResponse({"status": False, "errors": ["User is not active"]})
        else:
            return JsonResponse({"status": False, "errors": ["User doesn't exist"]})
    else:
        return render(request, 'login.html')

def logout_user(request):
    logout(request)
    return redirect('core:home')
