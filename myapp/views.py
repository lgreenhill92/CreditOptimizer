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




