from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from .models import InventoryItem


def get_jwt_token_for_user(user):
    refresh = RefreshToken.for_user(user)
    return str(refresh.access_token)


class InventoryItemListViewTests(APITestCase):

    def setUp(self):
        # Create a sample user and generate a JWT token
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.token = get_jwt_token_for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)

        # Create sample items in the database
        self.item1 = InventoryItem.objects.create(
            item_code="item123",
            item_name="Sample Item",
            description="This is a sample item",
            quantity=10,
            price=50,
        )
        self.item2 = InventoryItem.objects.create(
            item_code="item456",
            item_name="Another Item",
            description="This is another sample item",
            quantity=5,
            price=150,
        )

    def test_get_all_inventory_items(self):
        """Test retrieving all inventory items."""
        url = reverse("inventory_items")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]["item_code"], self.item1.item_code)

    def test_post_new_inventory_item(self):
        """Test creating a new inventory item."""
        url = reverse("inventory_items")
        data = {
            "item_code": "item789",
            "item_name": "New Item",
            "description": "This is a new item",
            "quantity": 15,
            "price": 150,
        }
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["item_code"], "item789")
        self.assertTrue(InventoryItem.objects.filter(item_code="item789").exists())

    def test_post_duplicate_inventory_item(self):
        """Test creating an item with a duplicate item_code."""
        url = reverse("inventory_items")
        data = {
            "item_code": self.item1.item_code,
            "item_name": "Duplicate Item",
            "description": "This item should not be created",
            "quantity": 20,
            "price": 150,
        }
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)


class InventoryItemDetailViewTests(APITestCase):

    def setUp(self):
        # Create a sample user and generate a JWT token
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.token = get_jwt_token_for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)

        # Create a sample item in the database
        self.item = InventoryItem.objects.create(
            item_code="item123",
            item_name="Sample Item",
            description="This is a sample item",
            quantity=10,
            price=150,
        )
        self.url = reverse("inventory_item_details", args=[self.item.id])

    def test_get_inventory_item(self):
        """Test retrieving a single inventory item by ID."""
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["item_code"], self.item.item_code)
        self.assertEqual(response.data["item_name"], self.item.item_name)

    def test_update_inventory_item(self):
        """Test updating an inventory item by ID."""
        data = {
            "item_code": "item123",
            "item_name": "Updated Item",
            "description": "This is an updated item",
            "quantity": 20,
            "price": 150,
        }
        response = self.client.put(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["item_name"], "Updated Item")
        self.assertEqual(response.data["quantity"], 20)

        # Refresh from database and check updated values
        self.item.refresh_from_db()
        self.assertEqual(self.item.item_name, "Updated Item")
        self.assertEqual(self.item.quantity, 20)

    def test_delete_inventory_item(self):
        """Test deleting an inventory item by ID."""
        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(InventoryItem.objects.filter(id=self.item.id).exists())
