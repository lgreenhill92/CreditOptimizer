from django.urls import path
from . import views

urlpatterns = [
    
     path('credit-cards/', views.credit_card_management, name='credit_card_management'),


    path('register/', views.register, name='register'),
    path("",views.home, name="home"),
    path("todos/", views.todos, name = "Todos"),
    path("login/", views.my_login, name = "login"),
    path("user_logout", views.user_logout, name = "user_logout"),

    path("about/", views.about, name = "about"),
    path("dashboard/", views.dashboard, name = "dashboard"),
    path("card_home/", views.card_home, name = "card_home"),
    path("add_card_transaction/", views.add_card_transaction, name = "add_card_transaction"),
    path("contact/", views.contact_page, name = "contact"),
    path("view_card_transactions/", views.view_card_transactions, name = "view_card_transactions")

]