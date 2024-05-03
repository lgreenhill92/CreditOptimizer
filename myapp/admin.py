# from django.contrib import admin
# from .models import TodoItem


# from django.contrib import admin
# from .models import CreditCard, Transaction

# admin.site.register(CreditCard)
# admin.site.register(Transaction)

from django.contrib import admin
from .models import CreditCard, Transaction

class CreditCardAdmin(admin.ModelAdmin):
    # Customize CreditCardAdmin as needed
    pass

class TransactionAdmin(admin.ModelAdmin):
    list_display = ['card', 'amount', 'date', 'get_user']

    def get_user(self, obj):
        return obj.card.user

    get_user.short_description = 'User'

admin.site.register(CreditCard, CreditCardAdmin)
admin.site.register(Transaction, TransactionAdmin)


