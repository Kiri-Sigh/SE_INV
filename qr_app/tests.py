# from django.test import TestCase, Client
# from django.urls import reverse
# from django.core.files.uploadedfile import SimpleUploadedFile
# from django.utils import timezone
# from .models import QRLog
# import json
# import base64
# from datetime import date, timedelta
# from cryptography.fernet import Fernet
# import os

# class QRLogModelTests(TestCase):
#     def setUp(self):
#         self.qr_log = QRLog.objects.create(
#             username="testuser",
#             locker_id="L123",
#             start_date=date.today(),
#             end_date=date.today() + timedelta(days=7),
#             qr_code=SimpleUploadedFile(
#                 name='test_qr.png',
#                 content=b'',  # Empty content for testing
#                 content_type='image/png'
#             )
#         )

#     def test_qr_log_creation(self):
#         self.assertEqual(self.qr_log.username, "testuser")
#         self.assertEqual(self.qr_log.locker_id, "L123")
#         self.assertEqual(self.qr_log.start_date, date.today())
#         self.assertEqual(self.qr_log.end_date, date.today() + timedelta(days=7))
#         self.assertTrue(self.qr_log.qr_code.name.startswith('qrcodes/'))
#         self.assertIsNotNone(self.qr_log.created_at)

#     def test_str_representation(self):
#         self.assertEqual(str(self.qr_log), "testuser - L123")

# class QRViewTests(TestCase):
#     @classmethod
#     def setUpClass(cls):
#         super().setUpClass()
#         cls.test_key = Fernet.generate_key()
#         with open("key.txt", "wb") as key_file:
#             key_file.write(cls.test_key)

#     @classmethod
#     def tearDownClass(cls):
#         super().tearDownClass()
#         if os.path.exists("key.txt"):
#             os.remove("key.txt")

#     def setUp(self):
#         self.client = Client()
#         self.cipher = Fernet(self.test_key)
#         self.data = {
#             'username': 'test',  # Short username
#             'locker_id': 'L1',   # Short locker_id
#             'start_date': '2024-03-20',
#             'end_date': '2024-03-21'
#         }

#     def test_generate_qr_get(self):
#         response = self.client.get(reverse('qr_app:generate_qr'))
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'qr_form.html')

#     def test_generate_qr_post(self):
#         response = self.client.post(reverse('qr_app:generate_qr'), self.data)
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'qr_form.html')
#         self.assertIn('qr_code', response.context)
        
#         # Verify that the QR code contains valid encrypted data
#         qr_code_base64 = response.context['qr_code']
#         self.assertTrue(isinstance(qr_code_base64, str))
#         self.assertTrue(len(qr_code_base64) > 0)

#     def test_log_data_post(self):
#         log_data = {
#             'username': 'testuser',
#             'locker_id': 'L123',
#             'action': 'open',
#             'timestamp': '2024-02-20 10:00:00'
#         }
#         response = self.client.post(
#             reverse('qr_app:log_data'),
#             data=json.dumps(log_data),
#             content_type='application/json'
#         )
#         self.assertEqual(response.status_code, 200)
#         response_data = json.loads(response.content)
#         self.assertEqual(response_data['status'], 'success')
        
#         # Verify log file content
#         with open('log.txt', 'r') as log_file:
#             last_line = log_file.readlines()[-1].strip()
#             self.assertIn('testuser', last_line)
#             self.assertIn('L123', last_line)
#             self.assertIn('open', last_line)

#     # def test_log_data_invalid_method(self):
#     #     response = self.client.get(reverse('qr_app:log_data'))
#     #     self.assertEqual(response.status_code, 405)
#     #     self.assertEqual(response['Content-Type'], 'application/json')

#     def test_log_data_invalid_data(self):
#         response = self.client.post(
#             reverse('qr_app:log_data'),
#             data='invalid json',
#             content_type='application/json'
#         )
#         self.assertEqual(response.status_code, 400)
#         response_data = json.loads(response.content)
#         self.assertEqual(response_data['status'], 'error')
