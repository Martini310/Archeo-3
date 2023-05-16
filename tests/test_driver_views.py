from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from kierowca.models import DriverOrder, Driver

class ViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.user2 = User.objects.create_user(username='testuser2', password='testpassword')
        self.order = DriverOrder.objects.create(orderer=self.user)
        self.driver = Driver.objects.create(first_name='John',
                                            last_name='Doe',
                                            pesel='93100808931',
                                            birth_date='2000-01-01',
                                            responsible_person=self.user,
                                            order=self.order,
                                            status='o')
        self.driver = Driver.objects.create(first_name='Jane',
                                            last_name='Doe',
                                            pesel='93100808931',
                                            birth_date='2000-01-01',
                                            responsible_person=self.user2,
                                            order=self.order,
                                            status='r')

    def test_list_view(self):
        url = reverse('kierowca:list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'kierowca/list.html')

    def test_search_view(self):
        url = reverse('kierowca:search')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'kierowca/search_results.html')

    def test_search_view_with_results(self):
        url = reverse('kierowca:search')
        data = {'search': 'John'}
        response = self.client.get(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'kierowca/search_results.html')
        self.assertContains(response, 'John')
        self.assertNotContains(response, 'Jane')

    def test_search_view_with_no_results(self):
        url = reverse('kierowca:search')
        data = {'search': 'Joe'}
        response = self.client.get(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'kierowca/search_results.html')
        self.assertNotContains(response, 'John')
        self.assertNotContains(response, 'Jane')

    def test_list_view_with_status_filter(self):
        url = reverse('kierowca:list')
        data = {'status': 'o'}
        response = self.client.get(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'kierowca/list.html')
        self.assertContains(response, 'John')
        self.assertNotContains(response, 'Jane')

    def test_list_view_with_user_filter(self):
        url = reverse('kierowca:list')
        data = {'user': self.user.id}
        response = self.client.get(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'kierowca/list.html')
        self.assertContains(response, 'John')
        self.assertNotContains(response, 'Jane')

