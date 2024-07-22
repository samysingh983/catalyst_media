from django.test import TestCase, Client
from django.urls import reverse
from .models import CatalystUser, File, Data
from django.core.files.uploadedfile import SimpleUploadedFile
import os
import tempfile
import pandas as pd

class ViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = CatalystUser.objects.create_user(username='testuser', email='test@example.com', password='testpassword')
        self.user.save()
        self.client.login(username='testuser', password='testpassword')
        
        # Create a temporary file for testing
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.csv')
        df = pd.DataFrame({
            'name': ['Company 1', 'Company 2'],
            'domain': ['domain1.com', 'domain2.com'],
            'year founded': [2000, 2001],
            'industry': ['Industry 1', 'Industry 2'],
            'size range': ['1-10', '11-50'],
            'locality': ['City 1, State 1, Country 1', 'City 2, State 2, Country 2'],
            'linkedin url': ['http://linkedin1.com', 'http://linkedin2.com'],
            'current employee estimate': [10, 20],
            'total employee estimate': [15, 25]
        })
        df.to_csv(self.temp_file.name, index=False)

    def tearDown(self):
        os.remove(self.temp_file.name)
        self.user.delete()

    def test_profile_view(self):
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')

    def test_register_view(self):
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')

    def test_delete_view(self):
        response = self.client.post(reverse('delete'), {'user_id': self.user.id})
        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        self.assertFalse(self.user.is_active)
        self.assertTemplateUsed(response, 'profile.html')

    def test_upload_file_view(self):
        with open(self.temp_file.name, 'rb') as file:
            response = self.client.post(reverse('upload_file'), {'file': file})
        self.assertEqual(response.status_code, 200)
        self.assertIn('file_id', response.json())

    def test_process_file_chunk_view(self):
        # First, upload the file
        with open(self.temp_file.name, 'rb') as file:
            response = self.client.post(reverse('upload_file'), {'file': file})
        file_id = response.json()['file_id']
        
        with open(self.temp_file.name, 'rb') as file:
            chunk = SimpleUploadedFile(file.name, file.read())
            response = self.client.post(reverse('process_file_chunk'), {
                'file_id': file_id,
                'file': chunk
            })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'Chunk uploaded successfully')

    def test_process_file_view(self):
        # First, upload the file
        with open(self.temp_file.name, 'rb') as file:
            response = self.client.post(reverse('upload_file'), {'file': file})
        file_id = response.json()['file_id']

        # Process the file
        response = self.client.post(reverse('process_file', kwargs={'file_id': file_id}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'success')
        file_instance = File.objects.get(id=file_id)
        self.assertEqual(file_instance.status, 'Processed')
        self.assertTrue(Data.objects.exists())

    def test_query_builder_view(self):
        response = self.client.get(reverse('query_builder'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'query_builder.html')
        self.assertIn('industries', response.context)
        self.assertIn('years', response.context)
        self.assertIn('cities', response.context)
        self.assertIn('states', response.context)
        self.assertIn('countries', response.context)

    def test_query_data_view(self):
        response = self.client.get(reverse('query_data'), {
            'keyword': 'Company 1',
            'industry': 'Industry 1',
            'year_founded': 2000,
            'city': 'City 1',
            'state': 'State 1',
            'country': 'Country 1',
            'employees_from': 5,
            'employees_to': 15
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('records_found', response.json())
        self.assertEqual(response.json()['records_found'], 1)
