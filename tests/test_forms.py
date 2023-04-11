from django.test import TestCase
from files.forms import MyOrderForm
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
            