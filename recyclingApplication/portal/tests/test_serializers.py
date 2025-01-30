from django.test import TestCase
from django.contrib.auth.models import User
from homepage.models import Request
from homepage.serializers import RequestSerializer
from django.utils.timezone import now

class RequestSerializerTest(TestCase):
    def setUp(self):
        """Set up test data before each test"""
        self.user = User.objects.create_user(username="testuser", password="testpassword")

        self.request_data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com",
            "phone": "1234567890",
            "address": "123 Street",
            "city": "New York",
            "state": "NY",
            "country": "USA",
            "postal_code": "10001",
            "status": "pending",
            "date_created": now(),
            "token": "abcd1234",
            "claimed_by": self.user.id,  # ForeignKey expects an ID
        }

        self.request_instance = Request.objects.create(
            **{**self.request_data, "claimed_by": self.user} 
        )

    def test_serializer_serialization(self):
        """Test if RequestSerializer correctly serializes data"""
        serializer = RequestSerializer(instance=self.request_instance)
        serialized_data = serializer.data

        self.assertEqual(serialized_data["first_name"], "John")
        self.assertEqual(serialized_data["last_name"], "Doe")
        self.assertEqual(serialized_data["email"], "john.doe@example.com")
        self.assertEqual(serialized_data["status"], "pending")
        self.assertEqual(serialized_data["claimed_by"], self.user.id)

    def test_serializer_deserialization(self):
        """Test if RequestSerializer correctly deserializes data"""
        serializer = RequestSerializer(data=self.request_data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        request_obj = serializer.save()

        self.assertEqual(request_obj.first_name, "John")
        self.assertEqual(request_obj.last_name, "Doe")
        self.assertEqual(request_obj.status, "pending")
        self.assertEqual(request_obj.claimed_by, self.user) 

    def test_invalid_serializer(self):
        """Test if serializer correctly handles invalid data"""
        invalid_data = self.request_data.copy()
        invalid_data["email"] = "invalid-email"  # Invalid email format

        serializer = RequestSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())  # Should not pass validation
        self.assertIn("email", serializer.errors)  # Ensure 'email' error exists
