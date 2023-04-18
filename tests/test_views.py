from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from django.utils import timezone
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


class OrdersToDoViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.user2 = User.objects.create_user(username='testuser2', password='testpass')

        self.order_a = Order.objects.create(order_date=timezone.now(), orderer=self.user)
        self.order_o = Order.objects.create(order_date=timezone.now(), orderer=self.user)
        self.order_r = Order.objects.create(order_date=timezone.now(), orderer=self.user)
        self.order_e = Order.objects.create(order_date=timezone.now(), orderer=self.user2)

        self.vehicle1_a = Vehicle.objects.create(tr='AB C123', responsible_person=self.user, status='a', order=self.order_a)
        self.vehicle2_a = Vehicle.objects.create(tr='XY Z789', responsible_person=self.user, status='a', order=self.order_a)

        self.vehicle3_o = Vehicle.objects.create(tr='ABC C123', responsible_person=self.user, status='o', order=self.order_o)
        self.vehicle4_o = Vehicle.objects.create(tr='XYC Z789', responsible_person=self.user, status='o', order=self.order_o)

        self.vehicle5_r = Vehicle.objects.create(tr='AB A123', responsible_person=self.user, status='r', order=self.order_r)
        self.vehicle6_r = Vehicle.objects.create(tr='XY A789', responsible_person=self.user, status='r', order=self.order_r)

        self.vehicle7_e = Vehicle.objects.create(tr='AB D123', responsible_person=self.user2, status='e', order=self.order_e)
        self.vehicle8_e = Vehicle.objects.create(tr='XY D789', responsible_person=self.user2, status='e', order=self.order_e)

        self.url = reverse('files:orders_to_do', args=['a'])

    def test_view_requires_login(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=' + self.url)

    def test_view_displays_orders_with_specified_status(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'files/orders_to_do.html')
        self.assertContains(response, 'Zamówienie nr {}'.format(self.order_a.id))
        self.assertContains(response, 'Liczba teczek 2')
        self.assertContains(response, self.user.username)

    def test_view_does_not_display_orders_with_different_status(self):
        self.client.login(username='testuser', password='testpass')
        url = reverse('files:orders_to_do', args=['e'])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'files/orders_to_do.html')
        self.assertContains(response, 'Zamówienie nr {}'.format(self.order_e.id))
        self.assertContains(response, 'Liczba teczek 2')
        self.assertContains(response, self.user.username)
