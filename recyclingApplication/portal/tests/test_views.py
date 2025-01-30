from django.test import TestCase
from django.urls import reverse

class LoginPageViewTest(TestCase):
    
    def test_login_view_status_code(self):
        # Test that the home view returns a status code 200.
        response = self.client.get(reverse('portal:portal_login'))
        self.assertEqual(response.status_code, 200)
    
    def test_login_view_contains_form(self):
        # Test that the login view contains the form in the response.
        response = self.client.get(reverse('portal:portal_login'))  
        
        # Check that the form is rendered and contains the expected form fields
        self.assertContains(response, '<form')  # Check for form tag presence
        self.assertContains(response, 'name="user_name"')  # Check for username input field
        self.assertContains(response, 'name="password"')  # Check for password input field

    def test_login_view_contains_text(self):
        # Test that the login view contains specific text (e.g., 'Login').
        response = self.client.get(reverse('portal:portal_login')) 
        
        # Check that the page contains the string 'Login'
        self.assertContains(response, 'Login')