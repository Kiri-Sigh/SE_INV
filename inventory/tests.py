# from django.test import TestCase, Client
# from django.urls import reverse
# from .models import ComponentCategory, CheapItem, ExpensiveItem, ExpensiveItemData
# from user.models import CustomUser
# from django.utils import timezone
# import uuid

# # Create your tests here.

# class ComponentCategoryTests(TestCase):
#     def setUp(self):
#         self.category = ComponentCategory.objects.create(
#             category="Electronics"
#         )

#     def test_category_creation(self):
#         self.assertEqual(self.category.category, "Electronics")
#         self.assertIsInstance(self.category.category_id, uuid.UUID)

# class CheapItemTests(TestCase):
#     def setUp(self):
#         self.category = ComponentCategory.objects.create(category="Electronics")
#         self.cheap_item = CheapItem.objects.create(
#             name="Resistor",
#             category=self.category,
#             stock=100,
#             description="Basic resistor",
#             quantity_available=90,
#             quantity_borrowed=10,
#             weight=1,
#             max_time=7,
#             amount_reserve=20,
#             percent_reserve=20,
#             requires_admin_approval=False
#         )

#     def test_cheap_item_creation(self):
#         self.assertEqual(self.cheap_item.name, "Resistor")
#         self.assertEqual(self.cheap_item.stock, 100)
#         self.assertEqual(self.cheap_item.quantity_available, 90)
#         self.assertEqual(self.cheap_item.quantity_borrowed, 10)

# class ExpensiveItemTests(TestCase):
#     def setUp(self):
#         self.category = ComponentCategory.objects.create(category="Equipment")
#         self.expensive_item = ExpensiveItem.objects.create(
#             name="Oscilloscope",
#             category=self.category,
#             stock=5,
#             description="Digital oscilloscope",
#             quantity_available=4,
#             quantity_borrowed=1,
#             component_status='P',
#             amount_reserve=1,
#             percent_reserve=20,
#             weight=5
#         )

#     def test_expensive_item_creation(self):
#         self.assertEqual(self.expensive_item.name, "Oscilloscope")
#         self.assertEqual(self.expensive_item.stock, 5)
#         self.assertEqual(self.expensive_item.max_time, 30)  # Default value
#         self.assertEqual(self.expensive_item.late_penalty, 100)  # Default value

# # class UserCartTests(TestCase):
# #     def setUp(self):
# #         self.user = CustomUser.objects.create_user(
# #             username="testuser",
# #             password="testpass123",
# #             email="test@example.com"
# #         )
# #         self.cart = UserCart.objects.create(user=self.user)
        
# #         # Create items for cart testing
# #         self.category = ComponentCategory.objects.create(category="Electronics")
# #         self.cheap_item = CheapItem.objects.create(
# #             name="LED",
# #             category=self.category,
# #             stock=50,
# #             description="LED light",
# #             quantity_available=45,
# #             quantity_borrowed=5,
# #             weight=1,
# #             amount_reserve=10,
# #             percent_reserve=20
# #         )
        
# #         self.expensive_item = ExpensiveItem.objects.create(
# #             name="Multimeter",
# #             category=self.category,
# #             stock=3,
# #             description="Digital multimeter",
# #             quantity_available=2,
# #             quantity_borrowed=1,
# #             component_status='P',
# #             amount_reserve=1,
# #             percent_reserve=20,
# #             weight=2
# #         )

# #     def test_cart_creation(self):
# #         self.assertEqual(self.cart.user, self.user)
# #         self.assertIsInstance(self.cart.cart_id, uuid.UUID)

# class ViewTests(TestCase):
#     def setUp(self):
#         self.client = Client()
#         self.category = ComponentCategory.objects.create(category="Electronics")
#         self.cheap_item = CheapItem.objects.create(
#             name="LED",
#             category=self.category,
#             stock=50,
#             description="LED light",
#             quantity_available=45,
#             quantity_borrowed=5,
#             weight=1,
#             amount_reserve=10,
#             percent_reserve=20
#         )
        
#         self.expensive_item = ExpensiveItem.objects.create(
#             name="Multimeter",
#             category=self.category,
#             stock=3,
#             description="Digital multimeter",
#             quantity_available=2,
#             quantity_borrowed=1,
#             component_status='P',
#             amount_reserve=1,
#             percent_reserve=20,
#             weight=2
#         )

#     def test_list_items_view(self):
#         response = self.client.get(reverse('inventory:list_items'))
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'item_list.html')
#         self.assertContains(response, "LED")
#         self.assertContains(response, "Multimeter")

#     def test_item_detail_view(self):
#         # Test cheap item detail
#         response = self.client.get(reverse('inventory:item_detail', 
#             args=[str(self.cheap_item.component_id)]))
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'item_detail.html')
#         self.assertContains(response, "LED")

#         # Test expensive item detail
#         response = self.client.get(reverse('inventory:item_detail', 
#             args=[str(self.expensive_item.component_id)]))
#         self.assertEqual(response.status_code, 200)
#         self.assertContains(response, "Multimeter")

#         # Test non-existent item
#         non_existent_id = uuid.uuid4()
#         response = self.client.get(reverse('inventory:item_detail', 
#             args=[str(non_existent_id)]))
#         self.assertEqual(response.status_code, 404)

#     def test_search_functionality(self):
#         # Test search with existing item
#         response = self.client.get(reverse('inventory:list_items') + '?q=LED')
#         self.assertEqual(response.status_code, 200)
#         self.assertContains(response, "LED")
#         self.assertNotContains(response, "Multimeter")

#         # Test search with non-existent item
#         response = self.client.get(reverse('inventory:list_items') + '?q=NonExistentItem')
#         self.assertEqual(response.status_code, 200)
#         self.assertNotContains(response, "LED")
#         self.assertNotContains(response, "Multimeter")
