from django.test import TestCase
from django.forms.models import model_to_dict
import unittest
from django.test import Client

# Create your tests here.

# need to get test item in json when visting /api/menu-items

from LittleLemonDRF.models import MenuItem

class MenuItemCase(TestCase):
    def setUp(self):
        MenuItem.objects.create(title="Grilled Fish", price=8.50, inventory=20)

    def test_MenuItem_Exists(self):
        """MenuItem existes after creation"""
        grilled_fish = MenuItem.objects.get(title="Grilled Fish")
        print(grilled_fish)
        grilled_fish_obj = {
            "id" : 1,
            "title" : "Grilled Fish",
            "price" : 8.50,
            "inventory" : 20
        }
        self.assertEqual(model_to_dict(grilled_fish), grilled_fish_obj)

class MenuItemListAPI(TestCase):
    def setUp(self):
        MenuItem.objects.create(title="Grilled Fish", price=8.50, inventory=20)
        MenuItem.objects.create(title = "Grilled Cheese", price = 3.50, inventory = 40)

        self.client = Client()
    def test_MenuItem_get_list(self):
        responce = self.client.get('/api/menu-items' , HTTP_ACCEPT='application/json')

        grilled_fish_obj = {
            "id" : 1,
            "title" : "Grilled Fish",
            "price" : '8.50', ## Why deos the decimal need to be a string?
            "inventory" : 20
        }
        grilled_cheese_obj = {
            "id" : 2,
            "title" : "Grilled Cheese",
            "price" : '3.50', ## Why deos the decimal need to be a string?
            "inventory" : 40
        }

        list_of_test_objs = [grilled_fish_obj, grilled_cheese_obj]


        self.assertEqual(responce.status_code, 200)
        self.assertEqual(responce.json(), list_of_test_objs)

    
    def test_MenuItem_get_one(self):
        responce_grilled_fish = self.client.get('/api/menu-items/1' , HTTP_ACCEPT='application/json')

        responce_grilled_cheese = self.client.get('/api/menu-items/2' , HTTP_ACCEPT='application/json')

        grilled_fish_obj = {
            "id" : 1,
            "title" : "Grilled Fish",
            "price" : '8.50', ## Why deos the decimal need to be a string?
            "inventory" : 20
        }
        grilled_cheese_obj = {
            "id" : 2,
            "title" : "Grilled Cheese",
            "price" : '3.50', ## Why deos the decimal need to be a string?
            "inventory" : 40
        }

        self.assertEqual(responce_grilled_fish.json(), grilled_fish_obj)
        self.assertEqual(responce_grilled_cheese.json(), grilled_cheese_obj)

    def test_MenuItem_Create_New_Item(self):
        responce = self.client.post('/api/menu-items', {'title' : 'Pizza', 'price' : '5.00', 'inventory' : '15'})

        pizza = {
            "id" : 3,
            "title" : "Pizza",
            "price" : '5.00', ## Why deos the decimal need to be a string?
            "inventory" : 15
        }
        
        
        self.assertEqual(responce.json(), pizza)
            
    def test_MenuItem_Create_New_Item_bad_price(self):
        responce = self.client.post('/api/menu-items', {'title' : 'Pizza', 'price' : '1.00', 'inventory' : '15'})

        error = {
            "price" : ['Ensure this value is greater than or equal to 2.']
        }
        
        
        self.assertEqual(responce.json(), error)

    def test_MenuItem_Create_New_Item_bad_inventory(self):
        responce = self.client.post('/api/menu-items', {'title' : 'Pizza', 'price' : '5.00', 'inventory' : '-2'})

        error = {
            "inventory" : ['Ensure this value is greater than or equal to 0.']
        }
        
        
        self.assertEqual(responce.json(), error)

    def test_MenuItem_Create_New_Item_both_bad_price_inventory(self):
        responce = self.client.post('/api/menu-items', {'title' : 'Pizza', 'price' : '1.00', 'inventory' : '-2'})

        error = {
            "price" : ['Ensure this value is greater than or equal to 2.'],
            "inventory" : ['Ensure this value is greater than or equal to 0.']
        }
        
        
        self.assertEqual(responce.json(), error)