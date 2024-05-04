
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import auth, User
from .decorators import login_required
from .forms import LoginForm, CreateUserForm, CreditCardForm, TransactionForm, UploadFileForm
from .models import TodoItem, CreditCard, CreditCardTransaction
import csv
from django.urls import reverse


# Views
def home(request):
    return render(request, "home.html")

def todos(request):
    items = TodoItem.objects.all()
    return render(request, "todos.html", {"todos": items})

def about(request):
    return render(request, "about.html")

def dashboard(request):
    if request.method == 'POST':
        if 'file' in request.FILES:
            handle_uploaded_file(request.FILES['file'], request.user)
            return redirect('credit_card_management')
    return render(request, "dashboard.html")

def card_home(request):
    return render(request, 'card_home.html')  # Replace 'card_home.html' with the actual template name


# # Create your views here.


# def login(request):
#     return render(request, "login.html")


def add_card_transaction(request):
    return render(request, "add_card_transaction.html")


def view_card_transactions(request):
    return render(request,"view_card_transactions.html" )

def contact_page(request):
    return render(request,"contact.html" )







@login_required
def credit_card_management(request):
    user_credit_cards = CreditCard.objects.filter(user=request.user)
    if request.method == 'POST':
        card_form = CreditCardForm(request.POST)
        if card_form.is_valid():
            credit_card = card_form.save(commit=False)
            credit_card.user = request.user
            credit_card.save()
            return redirect('credit_card_management')
    else:
        card_form = CreditCardForm()
    return render(request, 'credit_card_management.html', {'card_form': card_form, 'user_credit_cards': user_credit_cards})

def add_transaction(request, card_id):
    credit_card = CreditCard.objects.get(id=card_id)
    if request.method == 'POST':
        transaction_form = TransactionForm(request.POST)
        if transaction_form.is_valid():
            transaction = transaction_form.save(commit=False)
            transaction.card = credit_card
            transaction.save()
            return redirect('credit_card_management')
    else:
        transaction_form = TransactionForm()
    return render(request, 'add_transaction.html', {'transaction_form': transaction_form})

def my_login(request):
    form = LoginForm()

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('dashboard')

    context = {'loginform': form}
    return render(request, 'login.html', context=context)

def user_logout(request):
    logout(request)
    return redirect("home")

def register(request):
    form = CreateUserForm()

    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')

    context = {'registerfrom': form}
    return render(request, 'register.html', context=context)

def upload_file(request):
    print("started Received file:")
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        print("Received file FORM began validation")
        if form.is_valid():
            print("form is valid")
            handle_uploaded_file(request.FILES['file'], request.user)  # Pass the user object
            print("Received file DONE")  # Debugging: Print the name of the received file
            return redirect(reverse('credit_card_management'))
    else:
        form = UploadFileForm()
        print("Did not Receive file:")  # Debugging: Print the name of the received file
    return render(request, 'upload.html', {'form': form})


import csv
import io

def handle_uploaded_file(f, user):
    print("handle started")
    transactions = []
    
    # Wrap the file content in a text stream
    text_stream = io.StringIO(f.read().decode('utf-8'))
    
    # Use the text stream directly with csv.reader
    reader = csv.reader(text_stream)
    for row in reader:
        if len(row) < 6:
            continue
        trans_date = row[0]
        trans_desc = row[3]
        trans_amount = float(row[5]) if row[5].replace('.', '', 1).isdigit() else 0
        trans_category = row[4]
        trans_postdate = row[1]
        card_name = row[2]
        
        try:
            # Try to get the credit card object
            #credit_card = CreditCard.objects.get(user=user, card_number[-4:] = card_name)
            credit_card = CreditCard.objects.get(user=user, card_number__endswith=card_name)

        except CreditCard.DoesNotExist:
            # If it doesn't exist, handle it accordingly (skip or create)
            # For now, let's just skip the transaction
            print(f"Credit card '{card_name}' for user '{user}' does not exist. Skipping transaction.")
            continue
        
        # Adjust amount for payments/credits
        if trans_category == 'Payment/Credit':
            trans_amount = -float(row[6])
        transaction = CreditCardTransaction(
            card=credit_card,
            transaction_date=trans_date,
            posted_date=trans_postdate,
            description=trans_desc,
            category=trans_category,
            debit=trans_amount if trans_amount < 0 else None,
            credit=trans_amount if trans_amount > 0 else None
        )
        transactions.append(transaction)
        print(transaction)

    CreditCardTransaction.objects.bulk_create(transactions)



def dashboard(request):
     return render(request, "dashboard.html")







# from django.shortcuts import render
# from.models import TodoItem

# #new data added
# # views.py
# from django.shortcuts import render, redirect
# from django.contrib.auth import authenticate, login, logout
# from django.contrib import messages
# from .forms import LoginForm
# from django.contrib.auth.models import auth
# # views.py
# from django.shortcuts import render
# from .decorators import login_required
# # views.py
# from django.shortcuts import render, redirect
# from .forms import CreateUserForm, UserCreationForm


# # Create your views here.
# def home(request):
#     #return HttpResponse("Hello World!")
#     return render(request, "home.html")

# def todos(request):
#     items = TodoItem.objects.all()
#     return render(request, "todos.html", {"todos": items})

# def login(request):
#     return render(request, "login.html")



# def about(request):
#     return render(request, "about.html")

# def dashboard(request):
#      return render(request, "dashboard.html")

# def add_card_transaction(request):
#     return render(request, "add_card_transaction.html")

# def card_home(request):
#     return render(request, "card_home.html")

# def view_card_transactions(request):
#     return render(request,"view_card_transactions.html" )

# def contact_page(request):
#     return render(request,"contact.html" )




# def my_login(request):
#     form  = LoginForm()

#     if request.method == 'POST':

#         form = LoginForm(request, data = request.POST)
#         if form.is_valid():

#             username = request.POST.get('username')
#             password = request.POST.get('password')

#             user = authenticate(request, username=username, password=password)

#             if user is not None:
#                 auth.login(request, user)

#                 return redirect('dashboard')
            
#     context = {'loginform':form}
            
#     return render(request, 'login.html', context=context)



# def user_logout(request):
#     logout(request)
#     auth.logout(request)
#     # Redirect to a success page.
#     return redirect("home")


# def register(request):

#     form = CreateUserForm()

#     if request.method == "POST":

#         form = CreateUserForm(request.POST)

#         if form.is_valid():
#             form.save()

#             return redirect('login')
#     context = {'registerfrom':form}
#     return render(request, 'register.html', context= context)

# @login_required
# def my_view(request):
#     # Your view logic goes here
#     return render(request, 'my_template.html')

# # new backend implementation views.py
# # views.py///////////////////////////NOT USING
# from django.shortcuts import render
# from .models import CreditCard

# def credit_card_management(request):
#     if request.method == 'POST':
#         # Handle form submission and save credit card data
#         # Decrypt card number before saving
#         credit_card = CreditCard(
#             card_number=request.POST['card_number'],
#             card_expiry=request.POST['expiry_date'],  # Note: Changed to match HTML input name
#             # Add other fields as needed
#         )
#         credit_card.save()
#     # Fetch existing credit card data
#     credit_cards = CreditCard.objects.filter(user_id=request.user.id)
#     context = {'credit_cards': credit_cards}
#     return render(request, 'dashboard.html', context)  # Render the HTML template

# #/////////////////////////////////////////////////////

# # views.py

# from django.shortcuts import render, redirect
# from .models import CreditCard, Transaction
# from .forms import CreditCardForm, TransactionForm

# def credit_card_management(request):
#     user_credit_cards = CreditCard.objects.filter(user=request.user)
#     if request.method == 'POST':
#         card_form = CreditCardForm(request.POST)
#         if card_form.is_valid():
#             credit_card = card_form.save(commit=False)
#             credit_card.user = request.user
#             credit_card.save()
#             return redirect('credit_card_management')
#     else:
#         card_form = CreditCardForm()
#     return render(request, 'credit_card_management.html', {'card_form': card_form, 'user_credit_cards': user_credit_cards})

# def add_transaction(request, card_id):
#     credit_card = CreditCard.objects.get(id=card_id)
#     if request.method == 'POST':
#         transaction_form = TransactionForm(request.POST)
#         if transaction_form.is_valid():
#             transaction = transaction_form.save(commit=False)
#             transaction.card = credit_card
#             transaction.save()
#             return redirect('credit_card_management')
#     else:
#         transaction_form = TransactionForm()
#     return render(request, 'add_transaction.html', {'transaction_form': transaction_form})

# # updalod test for views.py
# # from django.shortcuts import render
# # from .forms import UploadFileForm
# # import csv

# # def handle_uploaded_file(f):
# #     # Process the uploaded file
# #     reader = csv.reader(f)
# #     for row in reader:
# #         # Do something with each row
# #         pass

# # def upload_file(request, card_id):
# #     if request.method == 'POST':
# #         form = UploadFileForm(request.POST, request.FILES)
# #         if form.is_valid():
# #             handle_uploaded_file(request.FILES['file'])
# #             # Redirect or render success message
# #             print("file saved"+card_id)
# #     else:
# #         form = UploadFileForm()
# #     return render(request, 'upload.html', {'form': form})
# #     #return HttpResponse("You're uploading file for card with ID %s." % card_id)

# from django.shortcuts import render, redirect
# from django.urls import reverse
# from .forms import UploadFileForm
# import csv

# def insert_transaction_into_db(self, data):
#         # Prepare the SQL query to insert the transaction data
#         query = """
#         INSERT INTO Card_Transactions 
#         (trans_date, trans_amount, trans_desc, trans_category, trans_postdate, card_name, card_id) 
#         VALUES (?, ?, ?, ?, ?, ?, ?)
#         """

#         # Execute the query for each item in the data
#         for item in data:
#             self.cursor.execute(query, item)

#         # Commit the changes and close the connection
#         self.conn.commit()

# def handle_uploaded_file(f):
#     # Process the uploaded file
#     transactions = []
#     reader = csv.reader(f)
#     for row in reader:
#         # Do something with each row
#         # For example, create a transaction for the card_id
#         # Ensure the row has the correct number of elements
#         if len(row) < 6:
#             continue

#         trans_date = row[0]
#         trans_desc = row[3]
        
#         # Check if the transaction amount is numeric
#         trans_amount = float(row[5]) if row[5].replace('.', '', 1).isdigit() else 0

#         trans_category = row[4]
#         trans_postdate = row[1]
#         card_name = row[2]
#         card_id = 1  # Replace with the actual card ID
        
#         # If it's a payment/credit, adjust the amount
#         if trans_category == 'Payment/Credit':
#             trans_amount = -float(row[6])

#         # Prepare transaction data
#         transaction = (trans_date, trans_amount, trans_desc, trans_category, trans_postdate, card_name, card_id)
#         transactions.append(transaction)


#         # Initialize Card_Transactions manager
#         card_transaction_manager = Card_Transactions()

#         # Insert data into the database
#         card_transaction_manager.insert_transaction_into_db(transactions)

#         pass

# def upload_file(request):
#     if request.method == 'POST':
#         form = UploadFileForm(request.POST, request.FILES)
#         if form.is_valid():
#             handle_uploaded_file(request.FILES['file'])
#             # Redirect to a success page
#             return redirect(reverse('credit_card_management'))  # Replace 'success_view' with the name of your success view
#     else:
#         form = UploadFileForm()
#     return render(request, 'upload.html', {'form': form})







