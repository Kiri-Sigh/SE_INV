from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.utils import timezone
import qrcode
import base64
from io import BytesIO
from cryptography.fernet import Fernet
import json

# Read the key from key.txt
with open("key.txt", "rb") as key_file:
    key = key_file.read()

cipher = Fernet(key)

@csrf_exempt
def generate_qr(request):
    if request.method == "POST":
        start_date = request.POST.get("start_date")
        end_date = request.POST.get("end_date")
        username = request.POST.get("username")
        locker_id = request.POST.get("locker_id")

        # Create JSON data
        data = {
            "start_date": start_date,
            "end_date": end_date,
            "username": username,
            "locker_id": locker_id
        }
        json_data = json.dumps(data).encode()

        # Encrypt the JSON data
        encrypted_data = cipher.encrypt(json_data)
        # encrypted_data = qr_str

        # Generate QR code
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(encrypted_data)
        qr.make(fit=True)
        img = qr.make_image(fill="black", back_color="white")

        # Convert QR code image to base64
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        img_str = base64.b64encode(buffer.getvalue()).decode()

        return render(request, "qr_form.html", {"qr_code": img_str})
    return render(request, "qr_form.html")

@csrf_exempt
def log_data(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            username = data.get("username")
            locker_id = data.get("locker_id")
            action = data.get("action")
            date_time_open = data.get("timestamp")

            # Log data to log.txt
            with open("log.txt", "a") as log_file:
                log_file.write(f"Username: {username}, DateTimeOpen: {date_time_open}, LockerID: {locker_id}, Action: {action}\n")

            return JsonResponse({"status": "success", "message": "Data logged successfully"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)
    return JsonResponse({"status": "error", "message": "Invalid request method"}, status=405)