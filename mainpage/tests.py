from django.test import TestCase
from django.test import Client

class Testtasks(TestCase):
    def setUp(self):
        self.client = Client() # мы создали подставного клиента вместо браузера 
    
    def test_create_task(self):
        self.client.post('/create/', {'title': 'test', 'description': 'test', 'date_start': 'test', 'deadline': 'test', 'repeat_type': 'test', 'repeat_i': 'test', 'done': 'test'})