# pylint: disable=no-member
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User, Permission
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

    def test_my_order_view_post_empty_form(self):
        # Create test data for the formset
        formset_data = {
            'form-TOTAL_FORMS': '10',
            'form-INITIAL_FORMS': '0',
            'form-MAX_NUM_FORMS': '1000'
        }

        response = self.client.post(reverse('files:my_order'), data=formset_data)
        self.assertEqual(response.status_code, 200) # Check if response is a page refresh

        # Check if a new order and vehicles haven't been created
        self.assertEqual(Order.objects.count(), 0)
        self.assertEqual(Vehicle.objects.count(), 0)

    def test_my_order_view_post_15_vehicles(self):
        # Create test data for the formset
        vehicles = {f'form-{n}-tr': f'AA 12{n}' for n in range(15)}
        formset_data = {
            'form-TOTAL_FORMS': '15',
            'form-INITIAL_FORMS': '0',
            'form-MAX_NUM_FORMS': '1000',
        } | vehicles

        response = self.client.post(reverse('files:my_order'), data=formset_data)
        self.assertEqual(response.status_code, 302) # Check if response is a redirect
        self.assertEqual(response.url, reverse('files:list')) # Check if it redirects to the correct URL

        # Check if a new order and vehicles have been created
        self.assertEqual(Order.objects.count(), 1)
        order = Order.objects.first()
        self.assertEqual(order.orderer, self.user)
        self.assertEqual(Vehicle.objects.count(), 15)

        vehicle_1 = Vehicle.objects.get(tr='AA 120')
        self.assertEqual(vehicle_1.order, order)
        self.assertEqual(vehicle_1.comments, '')

        vehicle_15 = Vehicle.objects.get(tr='AA 1214')
        self.assertEqual(vehicle_15.order, order)
        self.assertEqual(vehicle_15.comments, '')

    def test_my_order_view_post_empty_fields_between_vehicles(self):
        # Create test data for the formset
        formset_data = {
            'form-TOTAL_FORMS': '10',
            'form-INITIAL_FORMS': '0',
            'form-MAX_NUM_FORMS': '1000',
            'form-0-tr': 'AA 1234',
            'form-0-comments': 'Test comment 1',
            'form-1-tr': '',
            'form-1-comments': '',
            'form-2-tr': '',
            'form-2-comments': '',
            'form-3-tr': 'BB 1234',
            'form-3-comments': 'Test comment',
        }

        response = self.client.post(reverse('files:my_order'), data=formset_data)
        self.assertEqual(response.status_code, 302) # Check if response is a redirect
        self.assertEqual(response.url, reverse('files:list')) # Check if it redirects to the correct URL

        # Check if a new order and vehicles have been created
        self.assertEqual(Order.objects.count(), 1)
        order = Order.objects.first()
        self.assertEqual(order.orderer, self.user)
        self.assertEqual(Vehicle.objects.count(), 2)

        vehicle_1 = Vehicle.objects.get(tr='AA 1234')
        self.assertEqual(vehicle_1.order, order)
        self.assertEqual(vehicle_1.comments, 'Test comment 1')

        vehicle_2 = Vehicle.objects.get(tr='BB 1234')
        self.assertEqual(vehicle_2.order, order)
        self.assertEqual(vehicle_2.comments, 'Test comment')
        self.assertEqual(vehicle_2.pk, 2)

    def test_my_order_view_get(self):
        response = self.client.get(reverse('files:my_order'))
        self.assertEqual(response.status_code, 200) # Check if response is successful
        self.assertTemplateUsed(response, 'files/my_order.html') # Check if the correct template is used
        self.assertIsInstance(response.context['my_order_formset'], MyOrderFormSet) # Check if the formset is passed to the template


class OrdersToDoViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.user2 = User.objects.create_user(username='usertest', password='testpass')

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
        # Check if not logged user is redirected to login page
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=' + self.url)

    def test_view_require_permission(self):
        # Check if logged user has a permission to see Orders_to_do page
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_view_displays_orders_with_specified_status(self):
        self.user.user_permissions.add(Permission.objects.get(codename='view_order'))
        # Check if view displays only orders with vehicles with status 'a'(awaits)
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'files/orders_to_do.html')
        self.assertContains(response, f'Zamówienie nr {self.order_a.id}')
        self.assertContains(response, '<td id="do-realizacji">2</td>')
        self.assertContains(response, '<td id="ogółem">2</td>')

        self.assertContains(response, self.user.username)
        self.assertNotContains(response, f'Zamówienie nr {self.order_o.id}')
        self.assertNotContains(response, f'Zamówienie nr {self.order_r.id}')
        self.assertNotContains(response, f'Zamówienie nr {self.order_e.id}')

    def test_view_does_not_display_orders_with_different_status(self):
        self.user.user_permissions.add(Permission.objects.get(codename='view_order'))
        # Check if view properly displays filtered orders (vehicles with status 'e')
        self.client.login(username='testuser', password='testpass')
        url = reverse('files:orders_to_do', args=['e'])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'files/orders_to_do.html')
        self.assertContains(response, f'Zamówienie nr {self.order_e.id}')
        self.assertContains(response, '<td id="do-realizacji">0</td>')
        self.assertContains(response, '<td id="ogółem">2</td>')
        self.assertContains(response, self.user.username)
        self.assertNotContains(response, f'Zamówienie nr {self.order_o.id}')
        self.assertNotContains(response, f'Zamówienie nr {self.order_r.id}')
        self.assertNotContains(response, f'Zamówienie nr {self.order_a.id}')

    def test_view_properly_count_files_with_different_status(self):
        self.user.user_permissions.add(Permission.objects.get(codename='view_order'))
        self.client.login(username='testuser', password='testpass')

        Vehicle.objects.filter(pk=3).update(order=self.order_a)
        Vehicle.objects.filter(pk=5).update(order=self.order_a)
        Vehicle.objects.filter(pk=7).update(order=self.order_a)

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, f'Zamówienie nr {self.order_a.id}')
        self.assertContains(response, '<td id="do-realizacji">2</td>')
        self.assertContains(response, '<td id="ogółem">5</td>')

        self.assertNotContains(response, f'Zamówienie nr {self.order_o.id}')
        self.assertNotContains(response, f'Zamówienie nr {self.order_r.id}')
        self.assertNotContains(response, f'Zamówienie nr {self.order_e.id}')


class OrderDetailsViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')

        self.order = Order.objects.create(order_date=timezone.now(), orderer=self.user)

        self.vehicle1_a = Vehicle.objects.create(tr='AB C123', responsible_person=self.user, status='a', order=self.order)
        self.vehicle2_a = Vehicle.objects.create(tr='XY Z789', responsible_person=self.user, status='o', order=self.order)

        self.url = reverse('files:order_details', args=['1'])

    def test_view_requires_login(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=' + self.url)

    def test_view_require_permission(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403) # TODO incorect status
        # self.assertRedirects(response, '/accounts/login/?next=' + self.url)
        # response = self.client.get('/accounts/login/?next=' + self.url)
        # self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Nie masz dostępu do tej zawartości')

    def test_view_display_all_files(self):
        self.user.user_permissions.add(Permission.objects.get(codename='change_vehicle'))
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertRegex(response.content.decode(), r'<input class="form-check-input" type="checkbox" value="1" name="boxes" id="TestAll1">')
        self.assertNotRegex(response.content.decode(), r'<input class="form-check-input" type="checkbox" value="2" name="boxes" id="TestAll2">')


class NotificationContextTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.user2 = User.objects.create_user(username='testuser2', password='testpass')

        self.order = Order.objects.create(order_date=timezone.now(), orderer=self.user)

        self.vehicle1_a = Vehicle.objects.create(tr='AB C123', responsible_person=self.user, status='o', order=self.order, transfer_date=timezone.now())
        self.vehicle2_a = Vehicle.objects.create(tr='XY Z789', responsible_person=self.user, status='o', order=self.order, transfer_date=timezone.now())

        self.url = reverse('files:list')
    
    def test_user2_has_no_notifications(self):
        self.client.login(username='testuser2', password='testpass')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context.get('notifications').get('transfers')), 0)
        
    def test_user2_has_notifications(self):
        Vehicle.objects.all().update(transfering_to=self.user2)
        self.client.login(username='testuser2', password='testpass')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context.get('notifications').get('transfers')), 2)


class ReturnFormViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')
        self.url = reverse('files:return')

        self.order = Order.objects.create(order_date=timezone.now(), orderer=self.user)

        self.vehicle1 = Vehicle.objects.create(tr='AA 1234', responsible_person=self.user, status='o', order=self.order)
        self.vehicle2 = Vehicle.objects.create(tr='XY Z789', responsible_person=self.user, status='o', order=self.order)

    def test_user_has_no_permissions(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_user_has_permissions(self):
        self.user.user_permissions.add(Permission.objects.get(codename='return_vehicle'))
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'files/return.html')

    def test_return_file(self):
        self.user.user_permissions.add(Permission.objects.get(codename='return_vehicle'))
        self.time = timezone.now()

        # Create test data for the formset
        form_data = {
            'tr': 'AA 1234',
            'returner': self.user.pk,
            'comments': 'Test comment 1',
            'return_date': self.time,
        }
        self.client.post(reverse('files:return'), data=form_data)

        self.assertEqual(Vehicle.objects.get(tr='AA 1234').status, 'r')
        self.assertEqual(Vehicle.objects.get(tr='AA 1234').returner, self.user)
        self.assertEqual(Vehicle.objects.get(tr='AA 1234').comments, 'Test comment 1')
        self.assertEqual(Vehicle.objects.get(tr='AA 1234').return_date.today, self.time.today)


class TransferVehicleViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.order = Order.objects.create(order_date=timezone.now(), orderer=self.user)
        self.vehicle = Vehicle.objects.create(tr='AB C123',
                                              responsible_person=self.user,
                                              order=self.order,
                                              status='o',
                                              transfer_date=timezone.now())
        self.url = reverse('files:transfer', args=[self.vehicle.pk])

    def test_user_permissions(self):
        # Test that a non-owner user can't access the view
        other_user = User.objects.create_user(username='otheruser', password='12345')
        self.client.force_login(other_user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_view_form_fields(self):
        # Test that logged user with permissions see fields
        self.user.user_permissions.add(Permission.objects.get(codename='transfer_vehicle'))
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        form = response.context_data['form']
        self.assertIn('transfering_to', form.fields)
        self.assertIn('comments', form.fields)

    def test_transfer_vehicle(self):
        # Test that transfer file to new_user is succesful
        new_user = User.objects.create_user(username='newuser', password='12345')
        self.user.user_permissions.add(Permission.objects.get(codename='transfer_vehicle'))
        self.client.force_login(self.user)
        data = {
            'transfering_to': new_user.pk,
            'comments': 'Test transfer',
        }

        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 302)
        # print(response.context['form'].errors)
        self.vehicle.refresh_from_db()
        self.assertEqual(self.vehicle.transfering_to, new_user)
        self.assertEqual(self.vehicle.comments, 'Test transfer')


class ListUserVehiclesViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.order = Order.objects.create(order_date=timezone.now(), orderer=self.user)

        self.user2 = User.objects.create_user(username='usertest', password='testpass')
        self.order_2 = Order.objects.create(order_date=timezone.now(), orderer=self.user2)

        self.vehicle1 = Vehicle.objects.create(tr='AB C123', responsible_person=self.user, status='a', order=self.order)
        self.vehicle2 = Vehicle.objects.create(tr='XY Z789', responsible_person=self.user, status='r', order=self.order)
        self.vehicle3 = Vehicle.objects.create(tr='ABC C123', responsible_person=self.user, status='o', order=self.order)
        self.vehicle4 = Vehicle.objects.create(tr='XYC Z789', responsible_person=self.user, status='e', order=self.order)

        self.vehicle5 = Vehicle.objects.create(tr='AB A123', responsible_person=self.user2, status='a', order=self.order_2)
        self.vehicle6 = Vehicle.objects.create(tr='XY A789', responsible_person=self.user2, status='r', order=self.order_2)
        self.vehicle7 = Vehicle.objects.create(tr='AB D123', responsible_person=self.user2, status='o', order=self.order_2)
        self.vehicle8 = Vehicle.objects.create(tr='XY D789', responsible_person=self.user2, status='e', order=self.order_2)

        self.url = reverse('files:user_list')

    def test_login_required(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/files/user_list/')

    def test_user_has_only_self_vehicles(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'files/user_vehicles.html')

        self.assertContains(response, 'AB C123')
        self.assertContains(response, 'XY Z789')
        self.assertContains(response, 'ABC C123')
        self.assertContains(response, 'XYC Z789')

        self.assertNotContains(response, 'AB A123')
        self.assertNotContains(response, 'XY A789')
        self.assertNotContains(response, 'AB D123')
        self.assertNotContains(response, 'XY D789')

    def test_display_only_awaits_vehicles(self):
        self.client.login(username='testuser', password='testpass')
        self.url = reverse('files:user_list', args=['a'])
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, 'AB C123')

        self.assertNotContains(response, 'XY Z789')
        self.assertNotContains(response, 'ABC C123')
        self.assertNotContains(response, 'XYC Z789')

    def test_display_only_returned_vehicles(self):
        self.client.login(username='testuser', password='testpass')
        self.url = reverse('files:user_list', args=['r'])
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, 'XY Z789')

        self.assertNotContains(response, 'AB C123')
        self.assertNotContains(response, 'ABC C123')
        self.assertNotContains(response, 'XYC Z789')

    def test_display_only_onloan_vehicles(self):
        self.client.login(username='testuser', password='testpass')
        self.url = reverse('files:user_list', args=['o'])
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, 'ABC C123')

        self.assertNotContains(response, 'AB C123')
        self.assertNotContains(response, 'XY Z789')
        self.assertNotContains(response, 'XYC Z789')

    def test_display_only_rejected_vehicles(self):
        self.client.login(username='testuser', password='testpass')
        self.url = reverse('files:user_list', args=['e'])
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, 'XYC Z789')

        self.assertNotContains(response, 'AB C123')
        self.assertNotContains(response, 'XY Z789')
        self.assertNotContains(response, 'ABC C123')

    def test_display_vehicles_transfered_to_user2_in_user(self):
        # Test if vehicle transfered but not accepted is still in responsible user account
        Vehicle.objects.filter(id=3).update(transfering_to=self.user2)

        self.client.login(username='testuser', password='testpass')
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'ABC C123')

    def test_not_display_vehicles_transfered_to_user2(self):
        # Test if vehicle transfered but not accepted is not in 'transfering_to' user account
        self.client.login(username='usertest', password='testpass')
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'ABC C123')
