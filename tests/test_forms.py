from django.test import TestCase, Client
from files.forms import MyOrderForm, TransferForm
from files.models import Vehicle, User
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

    def test_transfer_to_another_user(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.user2 = User.objects.create_user(username='testuser2', password='testpass')

        self.client.login(username='testuser', password='testpass')
        # user = User.objects.create(username='test')
        # user2 = User.objects.create(username='test2')
        Vehicle.objects.create(tr='AA 12345', responsible_person=self.user, status='o')
        form = TransferForm(data={'transfering_to': self.user2})
        self.assertTrue(form.is_valid())
