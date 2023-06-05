# pylint: disable=no-member
from django.test import TestCase
from kierowca.forms import MyDriverOrderForm, TransferDriverForm
from kierowca.models import Driver, User
from django.utils import timezone
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
