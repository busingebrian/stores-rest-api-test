
import json
from models.store import StoreModel
from models.user import UserModel
from models.item import ItemModel
from tests.base_test import BaseTest


class ItemTest(BaseTest):
    def setUp(self):
        super(ItemTest, self).setUp()  # calling a method in super class in python
        with self.app() as client:
            with self.app_context():
                UserModel('test', '1234').save_to_db()  # creating a user in db

                # returns the access token i.e JWT
                auth_request = client.post('/auth', data=json.dumps({'username': 'test', 'password': '1234'}),
                                           headers={'content-type': 'application/json'})
                auth_token = json.loads(auth_request.data)['access_token']
                self.access_token = f'JWT {auth_token}'

    def test_get_item_no_auth(self):
        with self.app() as client:
            with self.app_context():
                resp = client.get('/item/test')

                self.assertEqual(resp.status_code, 401)

    def test_get_item_not_found(self):
        with self.app() as client:
            with self.app_context():
                # UserModel('test', '1234').save_to_db()  # creating a user in db
                #
                # # returns the access token i.e JWT
                # auth_request = client.post('/auth', data=json.dumps({'username': 'test', 'password': '1234'}),
                #                            headers={'content-type': 'application/json'})
                # auth_token = json.loads(auth_request.data)['access_token']
                # header = {'Authorization': 'JWT ' + auth_token}
                # #  for python3.6, the above can be written in the ff format
                # # header = {'Authorization': f'JWT {auth_token}'}

                resp = client.get('/item/test', headers={'Authorization': self.access_token})
                self.assertEqual(resp.status_code, 404)

    def test_get_item(self):
        with self.app() as client:
            with self.app_context():
                ItemModel('blazers22', 1400.0, 1).save_to_db()

                resp = client.get('/item/test', headers={'Authorization': self.access_token})
                self.assertEqual(resp.status_code, 404)

    def test_delete_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test', 19.99, 1).save_to_db()

                resp = client.delete('/item/test')

                self.assertEqual(resp.status_code, 200)
                self.assertDictEqual({'message': 'Item deleted'}, json.loads(resp.data))

    def test_create_item(self):
        with self.app() as client:
            with self.app_context():
                #  ItemModel('test', 19.99, 1).save_to_db()
                StoreModel('test').save_to_db()

                resp = client.post('/item/test', data={'price': 17.99, 'store_id': 1})

                self.assertEqual(resp.status_code, 201)
                self.assertDictEqual({'name': 'test', 'price': 17.99}, json.loads(resp.data))

    def test_create_duplicate_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test', 19.99, 1).save_to_db()

                resp = client.post('/item/test', data={'price': 19.99, 'store_id': 1})
                self.assertEqual(resp.status_code, 400)
                self.assertDictEqual({'message': "An item with name 'test' already exists."}, json.loads(resp.data))

    def test_put_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('collection').save_to_db()
                ItemModel('brian', 17.99, 1).save_to_db()

                resp = client.put('/item/brian', data={'price': 17.99, 'store_id': 1})

                self.assertEqual(resp.status_code, 200)
                self.assertEqual(ItemModel.find_by_name('brian').price, 17.99)
                self.assertDictEqual({'name': 'brian', 'price': 17.99}, json.loads(resp.data))

    def test_put_update_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test1').save_to_db()
                ItemModel('test', 16.99, 1).save_to_db()

                self.assertEqual(ItemModel.find_by_name('test').price, 16.99)  # testing if the item exists

                resp = client.put('/item/test', data={'price': 17.99, 'store_id': 1})  # updating the Item

                self.assertEqual(resp.status_code, 200)

                self.assertEqual(ItemModel.find_by_name('test').price, 17.99)
                self.assertDictEqual({'name': 'test', 'price': 17.99}, json.loads(resp.data))

    def test_item_list(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test1').save_to_db()
                ItemModel('test', 16.99, 1).save_to_db()

                resp = client.get('/items')

                self.assertDictEqual({'items': [{'name': 'test', 'price': 16.99}]}, json.loads(resp.data))





