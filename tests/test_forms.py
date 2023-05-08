from django.test import TestCase, Client
from files.forms import MyOrderForm, TransferForm
from files.models import Vehicle, User
from django.utils import timezone
# Create your tests here.

class MyOrderFormTest(TestCase):
        
    def test_file_is_taken(self):
        tr = 'PZ 12345'
        user = User.objects.create(username='test')
        Vehicle.objects.create(tr=tr, responsible_person=user, status='o')
        form = MyOrderForm(data={'tr': tr})
        self.assertFalse(form.is_valid())

    def test_file_is_returned(self):
        tr = 'PZ 12345'
        user = User.objects.create(username='test')
        Vehicle.objects.create(tr=tr, responsible_person=user, status='r')
        form = MyOrderForm(data={'tr': tr})
        self.assertTrue(form.is_valid())

    def test_file_is_rejected(self):
        tr = 'PZ 12345'
        user = User.objects.create(username='test')
        Vehicle.objects.create(tr=tr, responsible_person=user, status='e')
        form = MyOrderForm(data={'tr': tr})
        self.assertTrue(form.is_valid())

    def test_file_is_ordered(self):
        tr = 'PZ 12345'
        user = User.objects.create(username='test')
        Vehicle.objects.create(tr=tr, responsible_person=user, status='a')
        form = MyOrderForm(data={'tr': tr})
        self.assertFalse(form.is_valid())
        

class TransferFormTest(TestCase):
    
    def setUp(self):
        self.now = timezone.now()
        self.user1 = User.objects.create_user(username='user1', password='password')
        self.user2 = User.objects.create_user(username='user2', password='password')
        self.vehicle = Vehicle.objects.create(tr='123456789', transfer_date=self.now, responsible_person=self.user1)

    def test_valid_form(self):
        form_data = {
            'tr': '123456789',
            'transfer_date': self.now,
            'transfering_to': self.user2.pk,
            'comments': 'Some comments'
        }
        form = TransferForm(data=form_data, user=self.user1, instance=self.vehicle)
        # print(form.errors)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        form_data = {
            'tr': '123456789',
            'transfer_date': self.now,
            'transfering_to': self.user1.pk,  # Should exclude current user
            'comments': 'Some comments'
        }
        form = TransferForm(data=form_data, user=self.user1, instance=self.vehicle)
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)
        self.assertEqual(form.errors['transfering_to'], ['Select a valid choice. That choice is not one of the available choices.'])
