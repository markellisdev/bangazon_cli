import unittest
import sys
sys.path.append('../')
from app.ordermanager import *
from app.productonordermanager import *
from app.productmanager import *
from app.order import *
from app.product import *
from app.customer import *
from app.customerstatusmanager import *
from app.customerregistrar import *


class TestProductOnOrder(unittest.TestCase):
    """
    This class tests everything related to placing a product on an order.

    Method List
    test_customer_can_create_an_order
    test_customer_can_add_product_to_an_order
    test_customer_can_see_all_remaining_products_not_on_order
    Arguments unittest.TestCase allows the unittest model to know what to test.
    Author Zoe LeBlanc, Python Ponies
    """

    @classmethod
    def setUpClass(self):
        '''This method sets up initial instances of Customer, Product, OrderManger, ProductOnOrderManager, and Product Manager from the database'''
        with sqlite3.connect('../bangazon.db') as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM Products
                WHERE productId = {}
                """.format(3))
            selected_product = cursor.fetchone()
        cursor.close()
        self.active_user = Customer("zoe",  "343 paper street",  "nashville", "tn", "12345", "1234567")
        CustomerRegistrar.register(self.active_user, '../bangazon.db')
        status = CustomerStatusManager.change_status(self, self.active_user, 'bangazon.db')
        self.orderManager = OrderManager('../bangazon.db')
        self.productOnOrderManager = ProductOnOrderManager('../bangazon.db')
        self.productManager = ProductManager('../bangazon.db')
        self.product_1 = Product(selected_product[1], selected_product[2], selected_product[3], selected_product[4])
        self.order_1 = Order(self.active_user)
        self.orderManager.create_order(self.order_1)


    def test_customer_can_create_an_order(self):
        """ This method tests if a customer can successfully create an order. A customer should be able to create order after passing the user object.
        """
        self.assertIsInstance(self.order_1, Order)
        self.assertIsNotNone(self.orderManager.customer_has_active_order())

    def test_customer_can_add_product_to_an_order(self):
        """ This method tests if a customer can successfully add a product to an order. A customer should be able to add a product to an order by passing their product.
        """
        self.productOnOrderManager.add_product_to_order(self.product_1)
        product = self.productManager.get_one_product(self.product_1)
        products = self.productOnOrderManager.get_all_products_on_order()
        product_is_on_order = False
        for item in products:
            if item[1] == product[0]:
                product_is_on_order = True
        self.assertTrue(product_is_on_order)

    def test_remove_all_products_from_order(self):
        """This method tests if a customer can remove all products from their order"""
        self.productOnOrderManager.remove_all_products_from_order();
        all_products = self.productOnOrderManager.get_all_products_on_order()
        order_is_empty = False
        if len(all_products) == 0:
            order_is_empty = True
        self.assertTrue(order_is_empty)

    def test_customer_can_see_all_remaining_products_not_on_order(self):
        """ This method tests if a customer can successfully see products not on an order.
        """
        self.assertIsNotNone(self.productOnOrderManager.get_all_products_not_on_order())

    def test_customer_can_see_product_popularity(self):
        """ This method tests if a customer can successfully see products by popularity.
        """
        self.assertIsNotNone(self.productOnOrderManager.get_products_by_order_popularity())

if __name__ == '__main__':
    unittest.main()