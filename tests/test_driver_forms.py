# pylint: disable=no-member
from django.test import TestCase
from kierowca.forms import MyDriverOrderForm, TransferDriverForm, ReturnDriverForm, pesel_validation
from kierowca.models import Driver, User, DriverOrder
from django.utils import timezone
from django.core.exceptions import ValidationError
# Create your tests here.

class MyDriverOrderFormTest(TestCase):
    first_name = 'Jan'
    last_name = 'Kowalski'
    pesel = '12345678903'
    birth_date = '2000-01-01'
    kk = '1234/22'


    def test_file_is_taken(self):
        user = User.objects.create(username='test')
        Driver.objects.create(first_name=self.first_name,
                              last_name=self.last_name,
                              pesel=self.pesel,
                              birth_date=self.birth_date,
                              kk=self.kk,
                              responsible_person=user,
                              status='o')
        form = MyDriverOrderForm(data={'first_name': self.first_name,
                                       'last_name': self.last_name, 
                                       'pesel': self.pesel,
                                       'birth_date': self.birth_date,
                                       'kk': self.kk,
                                       })
        self.assertFalse(form.is_valid())

    def test_file_is_returned(self):
        user = User.objects.create(username='test')
        Driver.objects.create(first_name=self.first_name,
                              last_name=self.last_name,
                              pesel=self.pesel,
                              birth_date=self.birth_date,
                              kk=self.kk,
                              responsible_person=user,
                              status='r')
        
        form = MyDriverOrderForm(data={'first_name': self.first_name,
                                       'last_name': self.last_name, 
                                       'pesel': self.pesel,
                                       'birth_date': self.birth_date,
                                       'kk': self.kk,})
        
        self.assertTrue(form.is_valid())

    def test_file_is_rejected(self):
        user = User.objects.create(username='test')
        Driver.objects.create(first_name=self.first_name,
                              last_name=self.last_name,
                              pesel=self.pesel,
                              birth_date=self.birth_date,
                              kk=self.kk,
                              responsible_person=user,
                              status='e')
        
        form = MyDriverOrderForm(data={'first_name': self.first_name,
                                       'last_name': self.last_name, 
                                       'pesel': self.pesel,
                                       'birth_date': self.birth_date,
                                       'kk': self.kk,})
        
        self.assertTrue(form.is_valid())

    def test_file_is_ordered(self):
        user = User.objects.create(username='test')
        Driver.objects.create(first_name=self.first_name,
                              last_name=self.last_name,
                              pesel=self.pesel,
                              birth_date=self.birth_date,
                              kk=self.kk,
                              responsible_person=user,
                              status='a')
        
        form = MyDriverOrderForm(data={'first_name': self.first_name,
                                       'last_name': self.last_name, 
                                       'pesel': self.pesel,
                                       'birth_date': self.birth_date,
                                       'kk': self.kk,})
        
        self.assertFalse(form.is_valid())

    def test_driver_without_pesel(self):
        form = MyDriverOrderForm(data={'first_name': self.first_name,
                                       'last_name': self.last_name, 
                                       'birth_date': self.birth_date,
                                       'kk': self.kk,})
        
        self.assertTrue(form.is_valid())

    def test_driver_without_birth_date(self):
        form = MyDriverOrderForm(data={'first_name': self.first_name,
                                       'last_name': self.last_name,
                                       'pesel': self.pesel,
                                       'kk': self.kk,})
        
        self.assertFalse(form.is_valid())
        
    def test_driver_without_first_name(self):
        form = MyDriverOrderForm(data={'last_name': self.last_name,
                                       'pesel': self.pesel,
                                       'birth_date': self.birth_date,
                                       'kk': self.kk,})
        
        self.assertFalse(form.is_valid())

    def test_driver_without_last_name(self):
        form = MyDriverOrderForm(data={'first_name': self.first_name,
                                       'pesel': self.pesel,
                                       'birth_date': self.birth_date,
                                       'kk': self.kk,})
        
        self.assertFalse(form.is_valid())

    def test_wrong_date_format(self):
        form = MyDriverOrderForm(data={'first_name': self.first_name,
                                       'last_name': self.last_name, 
                                       'pesel': self.pesel,
                                       'birth_date': '2022-22-15',
                                       'kk': self.kk,})
        
        self.assertFalse(form.is_valid())

    def test_invalid_pesel(self):
        form = MyDriverOrderForm(data={'first_name': self.first_name,
                                       'last_name': self.last_name, 
                                       'pesel': 12345678900,
                                       'birth_date': self.birth_date,
                                       'kk': self.kk,})
        
        self.assertFalse(form.is_valid())


class TransferFormTest(TestCase):
    
    def setUp(self):
        self.now = timezone.now()
        self.user1 = User.objects.create_user(username='user1', password='password')
        self.user2 = User.objects.create_user(username='user2', password='password')
        self.driver = Driver.objects.create(first_name='Jan', last_name='Kowalski', pesel='12345678903', birth_date='2000-01-01', kk='1234/22', transfer_date=self.now, responsible_person=self.user1)

    def test_valid_form(self):
        form_data = {
            'first_name': 'Jan',
            'last_name': 'Kowalski',
            'pesel': '12345678903',
            'birth_date': '2000-01-01',
            'kk': '1234/22',
            'transfer_date': self.now,
            'transfering_to': self.user2.pk,
            'comments': 'Some comments'
        }
        form = TransferDriverForm(data=form_data, user=self.user1, instance=self.driver)
        # print(form.errors)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        form_data = {
            'first_name': 'Jan',
            'last_name': 'Kowalski',
            'pesel': '12345678903',
            'birth_date': '2000-01-01',
            'kk': '1234/22',
            'transfer_date': self.now,
            'transfering_to': self.user1.pk,  # Should exclude current user
            'comments': 'Some comments'
        }
        form = TransferDriverForm(data=form_data, user=self.user1, instance=self.driver)
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)
        self.assertEqual(form.errors['transfering_to'], ['Wybierz poprawną wartość. Podana nie jest jednym z dostępnych wyborów.'])


class ReturnDriverFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.order = DriverOrder.objects.create(orderer=self.user)
        self.driver1 = Driver.objects.create(first_name="JAN", last_name="NOWAK", pesel="12345678901", birth_date="1900-01-04", kk="", responsible_person=self.user, status='o', order=self.order)
    def test_valid_form_data(self):
        form_data = {
            'first_name': 'JAN',
            'last_name': 'NOWAK',
            'pesel': '12345678901',
            'returner': self.user.pk,
            'comments': 'Returned successfully',
        }
        form = ReturnDriverForm(data=form_data)
        # print(form.errors)
        self.assertTrue(form.is_valid())

    def test_invalid_form_data(self):
        # Missing required fields (returner)
        form_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'pesel': '12345678901',
            'comments': 'Returned successfully',
        }
        form = ReturnDriverForm(data=form_data)
        # print(form.errors)
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)
        self.assertIn('returner', form.errors)

        # Invalid pesel
        form_data['returner'] = self.user.pk
        form_data['pesel'] = '1234'  # Invalid pesel length
        form = ReturnDriverForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)
        self.assertIn('pesel', form.errors)

    def test_clean_pesel_with_valid_pesel(self):
        driver = Driver.objects.create(first_name='John', last_name='Doe', birth_date='2000-03-03', pesel='12345678901', status='o', responsible_person=self.user, order=self.order)
        form_data = {
            'pesel': '12345678901',
            'returner': self.user.pk,
        }
        form = ReturnDriverForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['pesel'], driver.pesel)

    def test_clean_pesel_with_invalid_pesel(self):
        form_data = {
            'pesel': '12345678905',
            'returner': self.user.pk,
        }
        form = ReturnDriverForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)
        self.assertIn('pesel', form.errors)


class PeselValidationTest(TestCase):
    def test_pesel_validation(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.order = DriverOrder.objects.create(orderer=self.user)

        self.driver1 = Driver.objects.create(first_name="JAN", last_name="NOWAK", pesel="12345678903", birth_date="1900-01-04", kk="", responsible_person=self.user, status='a', order=self.order)
        self.driver2 = Driver.objects.create(first_name="ADAM", last_name="KOWALSKI", pesel="11111111116", birth_date="2000-08-05", kk="65465/23", responsible_person=self.user, status='o', order=self.order)
        self.driver3 = Driver.objects.create(first_name="ANDRZEJ", last_name="JANIAK", pesel="22222222222", birth_date="1999-12-31", kk="", responsible_person=self.user, status='r', order=self.order)
        self.driver4 = Driver.objects.create(first_name="ROBERT", last_name="MAŁYSZ", pesel="33333333338", birth_date="2000-01-01", kk="564/2000", responsible_person=self.user, status='e', order=self.order)

        self.assertRaises(ValidationError, pesel_validation, '12345678903') # Driver is 'awaits'
        self.assertRaises(ValidationError, pesel_validation, '1234567890') # pesel to short
        self.assertRaises(ValidationError, pesel_validation, '123456789033') # pesel to long
        self.assertRaises(ValidationError, pesel_validation, '12345678901') # wrong checksum
        self.assertRaises(ValidationError, pesel_validation, '11111111116') # Driver is 'on loan'

