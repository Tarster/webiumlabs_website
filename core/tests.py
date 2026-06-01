import json
from django.test import TestCase, Client
from django.urls import reverse
from .models import ContactSubmission

class CoreViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.home_url = reverse('core:home')
        self.contact_url = reverse('core:contact')

    def test_home_page_loads(self):
        """Verify that the home page loads successfully and contains agency title text."""
        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, 200)
        # Verify content rendered by Jinja2 contains key signature words
        self.assertContains(response, 'WebiumLabs')
        self.assertContains(response, 'Agency')

    def test_contact_page_loads(self):
        """Verify that the contact page loads successfully and contains signature text."""
        response = self.client.get(self.contact_url)
        self.assertEqual(response.status_code, 200)
        # Verify content rendered by Jinja2 contains key signature words
        self.assertContains(response, 'Contact')
        self.assertContains(response, "We're Here To Help")

    def test_contact_submission_success_json(self):
        """Verify successful form submission via JSON payload."""
        payload = {
            'name': 'Alice Smith',
            'email': 'alice@example.com',
            'company': 'Altech Solutions',
            'service': 'Automation',
            'budget': '$10,000 - $25,000',
            'message': 'We want to build a real-time data dashboard using AI.'
        }
        response = self.client.post(
            self.contact_url,
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['success'])
        self.assertIn('sent successfully', data['message'])
        
        # Verify database record
        self.assertEqual(ContactSubmission.objects.count(), 1)
        sub = ContactSubmission.objects.first()
        self.assertEqual(sub.name, 'Alice Smith')
        self.assertEqual(sub.email, 'alice@example.com')
        self.assertEqual(sub.company, 'Altech Solutions')
        self.assertEqual(sub.service, 'Automation')
        self.assertEqual(sub.budget, '$10,000 - $25,000')
        self.assertEqual(sub.message, 'We want to build a real-time data dashboard using AI.')

    def test_contact_submission_success_form(self):
        """Verify successful form submission via standard Form POST."""
        payload = {
            'Name': 'Bob Jones',
            'Email': 'bob@example.com',
            'Company': 'Jones Tech',
            'Service': 'website creation',
            'Budget': 'Under $10,000',
            'message': 'We need a full brand redesign.'
        }
        response = self.client.post(self.contact_url, data=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['success'])
        
        # Verify database record
        self.assertEqual(ContactSubmission.objects.count(), 1)
        sub = ContactSubmission.objects.first()
        self.assertEqual(sub.name, 'Bob Jones')
        self.assertEqual(sub.email, 'bob@example.com')
        self.assertEqual(sub.company, 'Jones Tech')
        self.assertEqual(sub.service, 'website creation')
        self.assertEqual(sub.budget, 'Under $10,000')
        self.assertEqual(sub.message, 'We need a full brand redesign.')

    def test_contact_submission_missing_fields(self):
        """Verify submission fails when required fields are missing or invalid."""
        payload = {
            'name': '',
            'email': 'invalid-email',
            'service': 'Select Your Service',  # invalid selection
            'budget': 'None',
            'message': ''
        }
        response = self.client.post(
            self.contact_url,
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertFalse(data['success'])
        self.assertIn('errors', data)
        self.assertIn('name', data['errors'])
        self.assertIn('email', data['errors'])
        self.assertIn('service', data['errors'])
        self.assertIn('budget', data['errors'])
        self.assertIn('message', data['errors'])
        
        # Verify no database record was created
        self.assertEqual(ContactSubmission.objects.count(), 0)

    def test_page_404_view_loads(self):
        """Verify that the test 404 url loads successfully."""
        response = self.client.get('/404/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Page Not Found')
        self.assertContains(response, '404')
        self.assertContains(response, 'We can’t find the page you’re looking for.')

    def test_custom_handler404_triggers(self):
        """Verify that a non-existent URL triggers the custom handler404."""
        response = self.client.get('/this-path-does-not-exist-at-all/')
        self.assertEqual(response.status_code, 404)
        self.assertContains(response, 'Page Not Found', status_code=404)
