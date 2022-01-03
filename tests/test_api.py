from unittest import TestCase
from fastapi.testclient import TestClient

from app.main import app as web_app
from pprint import pprint
class APITestCate(TestCase):
    test_email = 'user22@invalid.com'
    def setUp(self) -> None:
        self.client = TestClient(web_app)
    
    def tearDown(self) -> None:
        pass
    
    def test_main_url(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 404)
    
    def test_create_user(self):
        user_data = {
            'user':{
                'email':self.test_email,
                'password':'123456',
                'first_name':'John',
                'last_name':'Doe',
                'nick_name':'JD'
            }
        }
        response = self.client.post('/user',json=user_data)
        self.assertEqual(response.status_code,200)
    
    def test_user_login(self):
        user_data = {
            "user_form": {
                "email": self.test_email,
                "password": '123456',
            }
        }
        response = self.client.post('/login',json=user_data)
        pprint(response.__dict__)
        self.assertEqual(response.status_code,200)
