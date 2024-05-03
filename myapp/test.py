# from django.test import TestCase

# import sqlite3
# from datetime import datetime

# # Connect to the database
# conn = sqlite3.connect('/Users/lancegreenhill/Documents/GitHub/demo/db.sqlite3')
# cursor = conn.cursor()

# # Function to add a credit card
# def add_credit_card(user_id, card_number, card_expiry, card_type, credit_limit, card_name, credit_apr, rewards):
#     query = """
#     INSERT INTO Credit_Cards 
#     (user_id, card_number, card_expiry, card_type, credit_limit, card_name, credit_apr, rewards) 
#     VALUES (?, ?, ?, ?, ?, ?, ?, ?)
#     """
#     cursor.execute(query, (user_id, card_number, card_expiry, card_type, credit_limit, card_name, credit_apr, rewards))
#     conn.commit()
#     print("Credit card added successfully.")

# # Function to add a transaction
# def add_transaction(card_id, transaction_date, merchant, amount, category):
#     query = """
#     INSERT INTO Transactions 
#     (card_id, transaction_date, merchant, amount, category) 
#     VALUES (?, ?, ?, ?, ?)
#     """
#     cursor.execute(query, (card_id, transaction_date, merchant, amount, category))
#     conn.commit()
#     print("Transaction added successfully.")

# # Example data
# user_id = 1
# card_number = "1234567890123456"
# card_expiry = "12/24"
# card_type = "Visa"
# credit_limit = 5000
# card_name = "My Visa Card"
# credit_apr = 0.18
# rewards = "Cashback"

# transaction_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
# merchant = "Online Store"
# amount = 100.0
# category = "Shopping"

# # Add credit card
# add_credit_card(user_id, card_number, card_expiry, card_type, credit_limit, card_name, credit_apr, rewards)

# # Get the card_id of the newly added credit card
# cursor.execute("SELECT card_id FROM Credit_Cards WHERE user_id = ? AND card_number = ?", (user_id, card_number))
# result = cursor.fetchone()
# if result:
#     card_id = result[0]
#     # Add transaction
#     add_transaction(card_id, transaction_date, merchant, amount, category)

# # Close the connection
# conn.close()

from django.test import TestCase
from django.contrib.auth import get_user_model
from myapp.models import CreditCard, Transaction
from datetime import datetime, timedelta
import random

class TestDataCreation(TestCase):
    def setUp(self):
        # Ensure that we have a user available for testing
        User = get_user_model()
        try:
            # Attempt to fetch the existing user
            self.user = User.objects.get(email='noah2021@gmail.com')
        except User.DoesNotExist:
            # If the user doesn't exist, create a new one
            self.user = User.objects.create_user(username='noah2021', email='noah2021@gmail.com', password='password')

        # Create 2 credit cards for the user
        self.credit_cards = []
        for _ in range(2):
            credit_card = CreditCard.objects.create(
                user=self.user,
                card_number='123456789012345{}'.format(random.randint(1000, 9999)),
                expiry_date='12/24',
                cvv='123'  # Assuming a default CVV value for simplicity
            )
            self.credit_cards.append(credit_card)
        
        # Add transactions for each credit card
        for card in self.credit_cards:
            for _ in range(20):
                transaction_date = datetime.now() - timedelta(days=random.randint(1, 365))
                Transaction.objects.create(
                    card=card,
                    amount=random.randint(10, 500),
                    date=transaction_date.date()
                )

    def test_data_creation(self):
        # Check if all data is created as expected
        self.assertEqual(get_user_model().objects.count(), 1)
        self.assertEqual(CreditCard.objects.count(), 2)
        self.assertEqual(Transaction.objects.count(), 40)  # 2 cards * 20 transactions each

