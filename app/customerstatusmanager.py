import sys
import sqlite3

class CustomerStatusManager():
    '''Method: changes user status from inactive to active
        Arguments: user, which indicates which user's status to change. Active = 1, inactive = 0.
        Author: L.Sales, Python Ponies
    '''

    def change_status(self, customer, db_path):
        with sqlite3.connect(db_path) as conn:
            c = conn.cursor()

            try:
                #change all users' status to inactive
                c.execute("UPDATE Customers SET active=0 WHERE active=1")
                #set the specified customer's status to active
                c.execute("UPDATE Customers SET active=1 WHERE customerId = '{}'".format(customer))
                #return that customer's status to the point of call
                c.execute("SELECT active FROM Customers WHERE active=1")
                status = c.fetchall()[0][0]
                return status
            except sqlite3.OperationalError:
                return "There was an error. Please try again."

