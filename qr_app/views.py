from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import QRLog
import qrcode
import io
import base64
import json
from cryptography.fernet import Fernet
import os

def get_encryption_key():
    try:
        with open("key.txt", "rb") as key_file:
            return key_file.read()
    except FileNotFoundError:
        # For testing purposes, generate a new key if file doesn't exist
        if os.environ.get('DJANGO_SETTINGS_MODULE') == 'prototype1.settings':
            key = Fernet.generate_key()
            with open("key.txt", "wb") as key_file:
                key_file.write(key)
            return key
        return Fernet.generate_key()

# Move key loading to a function
encryption_key = get_encryption_key()
cipher = Fernet(encryption_key)

def generate_qr(request):
    if request.method == 'POST':
        # Get form data
        username = request.POST.get('username')
        locker_id = request.POST.get('locker_id')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        # Create data string and encrypt it
        data = f"{username}|{locker_id}|{start_date}|{end_date}"
        encrypted_data = cipher.encrypt(data.encode())

        # Generate QR code
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(encrypted_data)
        qr.make(fit=True)
        qr_image = qr.make_image(fill_color="black", back_color="white")

        # Convert QR code to base64 string
        buffer = io.BytesIO()
        qr_image.save(buffer, format="PNG")
        qr_code_base64 = base64.b64encode(buffer.getvalue()).decode()

        # Save QR log
        # QRLog.objects.create(
        #     username=username,
        #     locker_id=locker_id,
        #     start_date=start_date,
            # end_date=end_date,
        #     qr_code=qr_code_base64
        # )

        return render(request, 'qr_form.html', {'qr_code': qr_code_base64})
    return render(request, 'qr_form.html')

@csrf_exempt
@require_http_methods(["POST"])
def log_data(request):
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)
    try:
        data = json.loads(request.body)
        # Log the data
        with open('log.txt', 'a') as log_file:
            log_file.write(f"{data['timestamp']} - User: {data['username']} - Locker: {data['locker_id']} - Action: {data['action']}\n")
        return JsonResponse({'status': 'success'})
    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)