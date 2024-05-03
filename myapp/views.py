from django.shortcuts import render
from.models import TodoItem

#new data added
# views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import LoginForm
from django.contrib.auth.models import auth
# views.py
from django.shortcuts import render
from .decorators import login_required
# views.py
from django.shortcuts import render, redirect
from .forms import CreateUserForm, UserCreationForm


# Create your views here.
def home(request):
    #return HttpResponse("Hello World!")
    return render(request, "home.html")

def todos(request):
    items = TodoItem.objects.all()
    return render(request, "todos.html", {"todos": items})

def login(request):
    return render(request, "login.html")



def about(request):
    return render(request, "about.html")

def dashboard(request):
     return render(request, "dashboard.html")

def add_card_transaction(request):
    return render(request, "add_card_transaction.html")

def card_home(request):
    return render(request, "card_home.html")

def view_card_transactions(request):
    return render(request,"view_card_transactions.html" )

def contact_page(request):
    return render(request,"contact.html" )




def my_login(request):
    form  = LoginForm()

    if request.method == 'POST':

        form = LoginForm(request, data = request.POST)
        if form.is_valid():

            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                auth.login(request, user)

                return redirect('dashboard')
            
    context = {'loginform':form}
            
    return render(request, 'login.html', context=context)



def user_logout(request):
    logout(request)
    auth.logout(request)
    # Redirect to a success page.
    return redirect("home")


def register(request):

    form = CreateUserForm()

    if request.method == "POST":

        form = CreateUserForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect('login')
    context = {'registerfrom':form}
    return render(request, 'register.html', context= context)

@login_required
def my_view(request):
    # Your view logic goes here
    return render(request, 'my_template.html')

# new backend implementation views.py
# views.py///////////////////////////NOT USING
from django.shortcuts import render
from .models import CreditCard

def credit_card_management(request):
    if request.method == 'POST':
        # Handle form submission and save credit card data
        # Decrypt card number before saving
        credit_card = CreditCard(
            card_number=request.POST['card_number'],
            card_expiry=request.POST['expiry_date'],  # Note: Changed to match HTML input name
            # Add other fields as needed
        )
        credit_card.save()
    # Fetch existing credit card data
    credit_cards = CreditCard.objects.filter(user_id=request.user.id)
    context = {'credit_cards': credit_cards}
    return render(request, 'dashboard.html', context)  # Render the HTML template

#/////////////////////////////////////////////////////

# views.py

from django.shortcuts import render, redirect
from .models import CreditCard, Transaction
from .forms import CreditCardForm, TransactionForm

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








