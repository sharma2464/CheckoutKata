import unittest
from main import Cart, Item


class TestSuite(unittest.TestCase):
    def setup(self):
        self.cart = Cart()

    def test_add_item(self):
        new_item = {
            "tag": "A",
            "name": "Apple",
            "price": 50,
            "discount": {"special_price": 130, "quantity": 3}
        }

        self.cart.add_item(new_item)
        self.assertEqual(len(self.cart.items), 1)



if __name__ == '__main__':
    unittest.main()