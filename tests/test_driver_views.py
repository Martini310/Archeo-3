# pylint: disable=no-member
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User, Permission
from kierowca.models import DriverOrder, Driver
from django.utils import timezone
from datetime import datetime

class ListViewTestCase(TestCase):
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


class AddDriverViewTest(TestCase):
    def test_add_driver(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.order = DriverOrder.objects.create(orderer=self.user)
        self.client.login(username='testuser', password='testpassword')
        self.time = datetime(2002, 5, 15)

        # Define the URL for the add driver view
        url = reverse('kierowca:add')

        # Simulate a POST request with form data
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'pesel': '12345678903', 
            'order': self.order.id,
            'birth_date': self.time.date(),
            'responsible_person': self.user.pk,
        }
        response = self.client.post(url, data, follow=True)

        # Assert that the driver was created successfully
        self.assertEqual(response.status_code, 200)  # Check for a redirect
        self.assertEqual(Driver.objects.count(), 1)

        # Assert that the driver's attributes are correct
        driver = Driver.objects.first()
        self.assertEqual(driver.first_name, 'John')
        self.assertEqual(driver.last_name, 'Doe')
        self.assertEqual(driver.pesel, '12345678903')
        self.assertEqual(driver.birth_date, self.time.date())
        self.assertEqual(driver.order.id, 1)
        self.assertEqual(driver.responsible_person, self.user)
        # Assert the redirect URL after successful creation
        self.assertRedirects(response, reverse('kierowca:list'))


class MyDriverOrderViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        self.url = reverse('kierowca:my_driverorder')

    def test_get_request(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'kierowca/my_driverorder.html')
        self.assertContains(response, 'Zamówienie na teczki')

    def test_post_request_valid_data(self):
        data = {
            'form-TOTAL_FORMS': '1',
            'form-INITIAL_FORMS': '0',
            'form-MIN_NUM_FORMS': '0',
            'form-MAX_NUM_FORMS': '1000',
            'form-0-first_name': 'John',
            'form-0-last_name': 'Doe',
            'form-0-pesel': '12345678903',
            'form-0-birth_date': '2000-01-01',
            'form-0-comments': 'Some comments',
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('kierowca:list'))

        # Verify that the order and driver were created
        self.assertTrue(DriverOrder.objects.exists())
        self.assertTrue(Driver.objects.exists())

        order = DriverOrder.objects.first()
        driver = Driver.objects.first()

        self.assertEqual(driver.first_name, 'John')
        self.assertEqual(driver.last_name, 'Doe')
        self.assertEqual(driver.pesel, '12345678903')
        self.assertEqual(driver.birth_date.strftime('%Y-%m-%d'), '2000-01-01')
        self.assertEqual(driver.comments, 'Some comments')
        self.assertEqual(driver.order, order)

    def test_post_request_invalid_data(self):
        data = {
            'form-TOTAL_FORMS': '1',
            'form-INITIAL_FORMS': '0',
            'form-MIN_NUM_FORMS': '0',
            'form-MAX_NUM_FORMS': '1000',
            'form-0-first_name': 'John',
            'form-0-last_name': 'Doe',
            'form-0-pesel': '12345',  # Invalid PESEL
            'form-0-birth_date': '2000-01-01',
            'form-0-comments': 'Some comments',
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'kierowca/my_driverorder.html')
        self.assertFormsetError(response, 'my_driverorder_formset', 0, 'pesel', 'Pesel musi mieć 11 znaków')

        # Verify that no order or driver was created
        self.assertFalse(DriverOrder.objects.exists())
        self.assertFalse(Driver.objects.exists())


class DriverOrdersToDoViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.user2 = User.objects.create_user(username='usertest', password='testpass')

        self.order_a = DriverOrder.objects.create(order_date=timezone.now(), orderer=self.user)
        self.order_o = DriverOrder.objects.create(order_date=timezone.now(), orderer=self.user)
        self.order_r = DriverOrder.objects.create(order_date=timezone.now(), orderer=self.user)
        self.order_e = DriverOrder.objects.create(order_date=timezone.now(), orderer=self.user2)

        self.driver1_a = Driver.objects.create(first_name="JAN", last_name="NOWAK", pesel="12345678903", birth_date="1900-01-04", kk="", responsible_person=self.user, status='a', order=self.order_a)
        self.driver2_a = Driver.objects.create(first_name="ADAM", last_name="KOWALSKI", pesel="11111111116", birth_date="2000-08-05", kk="65465/23", responsible_person=self.user, status='a', order=self.order_a)

        self.driver3_o = Driver.objects.create(first_name="ANDRZEJ", last_name="JANIAK", pesel="22222222222", birth_date="1999-12-31", kk="", responsible_person=self.user, status='o', order=self.order_o)
        self.driver4_o = Driver.objects.create(first_name="ROBERT", last_name="MAŁYSZ", pesel="33333333338", birth_date="2000-01-01", kk="564/2000", responsible_person=self.user, status='o', order=self.order_o)

        self.driver5_r = Driver.objects.create(first_name="ANNA", last_name="NOWAK", pesel="44444444444", birth_date="1959-04-29", kk="", responsible_person=self.user, status='r', order=self.order_r)
        self.driver6_r = Driver.objects.create(first_name="HANNA", last_name="KOWALSKA", pesel="5555555550", birth_date="1993-08-19", kk="56454/2012", responsible_person=self.user, status='r', order=self.order_r)

        self.driver7_e = Driver.objects.create(first_name="MARZENA", last_name="DUDA", pesel="66666666666", birth_date="2011-05-30", kk="", responsible_person=self.user2, status='e', order=self.order_e)
        self.driver8_e = Driver.objects.create(first_name="PAULINA", last_name="BŁASZAK", pesel="77777777772", birth_date="2005-11-30", kk="", responsible_person=self.user2, status='e', order=self.order_e)

        self.url = reverse('kierowca:orders_to_do', args=['a'])

    def test_view_requires_login(self):
        # Check if not logged user is redirected to login page
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=' + self.url)

    def test_view_require_permission(self):
        # Check if logged user has a permission to see Orders_to_do page
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    # TODO
    # def test_view_displays_orders_with_specified_status(self):
    #     self.user.user_permissions.add(Permission.objects.get(codename='view_order'))
    #     # Check if view displays only orders with vehicles with status 'a'(awaits)
    #     self.client.login(username='testuser', password='testpass')
    #     response = self.client.get(self.url)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'pojazd/orders_to_do.html')
    #     self.assertContains(response, f'Zamówienie nr {self.order_a.id}')
    #     self.assertContains(response, '<td id="do-realizacji">2</td>')
    #     self.assertContains(response, '<td id="ogółem">2</td>')

    #     self.assertContains(response, self.user.username)
    #     self.assertNotContains(response, f'Zamówienie nr {self.order_o.id}')
    #     self.assertNotContains(response, f'Zamówienie nr {self.order_r.id}')
    #     self.assertNotContains(response, f'Zamówienie nr {self.order_e.id}')

    # def test_view_does_not_display_orders_with_different_status(self):
    #     self.user.user_permissions.add(Permission.objects.get(codename='view_order'))
    #     # Check if view properly displays filtered orders (vehicles with status 'e')
    #     self.client.login(username='testuser', password='testpass')
    #     url = reverse('pojazd:orders_to_do', args=['e'])
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'pojazd/orders_to_do.html')
    #     self.assertContains(response, f'Zamówienie nr {self.order_e.id}')
    #     self.assertContains(response, '<td id="do-realizacji">0</td>')
    #     self.assertContains(response, '<td id="ogółem">2</td>')
    #     self.assertContains(response, self.user.username)
    #     self.assertNotContains(response, f'Zamówienie nr {self.order_o.id}')
    #     self.assertNotContains(response, f'Zamówienie nr {self.order_r.id}')
    #     self.assertNotContains(response, f'Zamówienie nr {self.order_a.id}')

    # def test_view_properly_count_files_with_different_status(self):
    #     self.user.user_permissions.add(Permission.objects.get(codename='view_order'))
    #     self.client.login(username='testuser', password='testpass')

    #     Vehicle.objects.filter(pk=3).update(order=self.order_a)
    #     Vehicle.objects.filter(pk=5).update(order=self.order_a)
    #     Vehicle.objects.filter(pk=7).update(order=self.order_a)

    #     response = self.client.get(self.url)
    #     self.assertEqual(response.status_code, 200)

    #     self.assertContains(response, f'Zamówienie nr {self.order_a.id}')
    #     self.assertContains(response, '<td id="do-realizacji">2</td>')
    #     self.assertContains(response, '<td id="ogółem">5</td>')

    #     self.assertNotContains(response, f'Zamówienie nr {self.order_o.id}')
    #     self.assertNotContains(response, f'Zamówienie nr {self.order_r.id}')
    #     self.assertNotContains(response, f'Zamówienie nr {self.order_e.id}')