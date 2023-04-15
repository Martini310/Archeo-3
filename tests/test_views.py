from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import datetime, timedelta

from files.models import Order, Vehicle
from files.forms import MyOrderFormSet


class MyOrderViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')


    def test_my_order_view_post(self):
        # Create test data for the formset
        formset_data = {
            'form-TOTAL_FORMS': '10',
            'form-INITIAL_FORMS': '0',
            'form-MAX_NUM_FORMS': '1000',
            'form-0-tr': 'Te st1',
            'form-0-comments': 'Test comment 1',
            'form-1-tr': 'Te st2',
            'form-1-comments': 'Test comment 2',
            'form-2-tr': '',
            'form-2-comments': '',
        }

        response = self.client.post(reverse('files:my_order'), data=formset_data)
        self.assertEqual(response.status_code, 302) # Check if response is a redirect
        self.assertEqual(response.url, reverse('files:list')) # Check if it redirects to the correct URL

        # Check if a new order and vehicles have been created
        self.assertEqual(Order.objects.count(), 1)
        order = Order.objects.first()
        self.assertEqual(order.orderer, self.user)
        self.assertEqual(Vehicle.objects.count(), 2)

        vehicle_1 = Vehicle.objects.get(tr='Te st1')
        self.assertEqual(vehicle_1.order, order)
        self.assertEqual(vehicle_1.comments, 'Test comment 1')

        vehicle_2 = Vehicle.objects.get(tr='Te st2')
        self.assertEqual(vehicle_2.order, order)
        self.assertEqual(vehicle_2.comments, 'Test comment 2')

    def test_my_order_view_get(self):
        response = self.client.get(reverse('files:my_order'))
        self.assertEqual(response.status_code, 200) # Check if response is successful
        self.assertTemplateUsed(response, 'files/my_order.html') # Check if the correct template is used
        self.assertIsInstance(response.context['my_order_formset'], MyOrderFormSet) # Check if the formset is passed to the template