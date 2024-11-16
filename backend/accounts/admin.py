from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Cryptocurrency, Transaction, Wallet
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages

# class CustomAdminSite(AdminSite):
#     # login_form = CustomAdminAuthenticationForm
#     # login_template = 'admin/login.html'

# class UserAdmin(BaseUserAdmin):
#     list_display = ('email', 'first_name', 'last_name', 'is_staff', 'is_superuser')
#     list_filter = ('is_staff', 'is_superuser')
#     fieldsets = ( (None, {'fields': ('email', 'password')}),
#         ('Personal info', {'fields': ('first_name', 'last_name', 'email',)}),
#         ('Permissions', {'fields': ( 'is_active', 'is_staff', 'is_superuser')}),
#         ('Important dates', {'fields': ('last_login', ),}),
#     )
#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('email', 'first_name', 'last_name', 'email', 'password1', 'password2'),
#         }),
#     )
#     search_fields = ('email', 'first_name', 'last_name')
#     ordering = ('email',)
#     filter_horizontal = ()

# custom_admin_site = CustomAdminSite(name='custom_admin')


class TransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'plan', 'crypto', 'status', 'transaction_id', 'timestamp')
    list_filter = ('status', 'plan', 'crypto')
    search_fields = ('user_username', 'transaction_id')
    actions = ['mark_as_confirmed', 'mark_as_failed']

    # Action to mark transactions as confirmed
    def mark_as_confirmed(self, request, queryset):
        """Admin action to mark selected transactions as confirmed and update the user's wallet balance."""
        try:
            queryset.update(status='SUCCESS')
            for transaction in queryset:
                if transaction.status == 'SUCCESS':
                    wallet = transaction.user.wallet_set.filter(crypto=transaction.crypto).first()
                    user = transaction.user
                    print(user)
                    wallet = Wallet.objects.get(user=user)
                    if wallet:
                        wallet.balance += transaction.amount
                        wallet.save()

                        # Notify user that their deposit has been confirmed
                        subject = f"Deposit Confirmed for {transaction.plan} Plan"
                        message = (f"Dear {transaction.user.get_full_name},\n\n"
                                   f"Your deposit of ${transaction.amount} for the {transaction.plan} plan "
                                   f"has been confirmed and your wallet balance has been updated.\n\n"
                                   f"Thank you for choosing our service.\n\n"
                                   f"Best regards,\n{settings.COMPANY_NAME} Team")
                        
                        send_mail(
                            subject,
                            message,
                            settings.DEFAULT_FROM_EMAIL,
                            [transaction.user.email],
                            fail_silently=True,
                        )

            self.message_user(request, "Selected transactions have been marked as confirmed.")
        
        except Exception as e:
            messages.error(request, f"An error occurred while confirming transactions: {str(e)}")

    # Action to mark transactions as failed
    def mark_as_failed(self, request, queryset):
        queryset.update(status='FAILED')
        self.message_user(request, "Selected transactions have been marked as failed.")

    mark_as_confirmed.short_description = "Mark selected transactions as Confirmed"
    mark_as_failed.short_description = "Mark selected transactions as Failed"

admin.site.register(Transaction, TransactionAdmin)


admin.site.register(User)
admin.site.register(Cryptocurrency)
admin.site.register(Wallet)