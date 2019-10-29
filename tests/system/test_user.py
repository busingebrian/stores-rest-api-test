from models.user import UserModel
from tests.base_test import BaseTest
import json  # json comes with python lib that converts dictionaries to json to send our API


class UserTest(BaseTest):
    def test_register_user(self):
        with self.app() as client:
            with self.app_context():  # this helps to store & retrieve data from the db
                response = client.post('/register', data={'username': 'test', 'password': '1234'})

                self.assertEqual(response.status_code, 201)
                self.assertIsNotNone(UserModel.find_by_username('test'))
                self.assertDictEqual({'message': 'User created successfully'}, json.loads(response.data))

    def test_reg_and_login(self):
        with self.app() as client:
            with self.app_context():  # this helps to store & retrieve data from the db
                client.post('/register', data={'username': 'test', 'password': '1234'})
                auth_response = client.post('/auth',
                                            data=json.dumps({'username': 'test', 'password': '1234'}),
                                            headers={'Content-Type': 'application/json'})
                # converts the string to a valid json string

                self.assertIn('access_token', json.loads(auth_response.data).keys())
                # returns smethg like --> ['access_token']

    def test_reg_duplicate_user(self):
        with self.app() as client:
            with self.app_context():  # this helps to store & retrieve data from the db
                client.post('/register', data={'username': 'test', 'password': '1234'})

                response = client.post('/register', data={'username': 'test', 'password': '1234'})

                self.assertEqual(response.status_code, 400)
                self.assertDictEqual({'message': 'A user with that username already exists'}, json.loads(response.data))
