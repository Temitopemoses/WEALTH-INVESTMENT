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
    list_display = ('user', 'amount', 'transaction_type', 'plan', 'crypto', 'status', 'transaction_id', 'timestamp')
    list_filter = ('status', 'plan', 'crypto')
    search_fields = ('user_username', 'transaction_id')
    actions = ['mark_as_confirmed', 'mark_as_failed', "approve_withdrawals"]

    # Action to mark transactions as confirmed
    def mark_as_confirmed(self, request, queryset):
        """Admin action to mark selected transactions as confirmed and update the user's wallet balance."""
        try:
            queryset.update(status='SUCCESS')
            for transaction in queryset:
                if transaction.status == 'SUCCESS':
                    # wallet = transaction.user.wallet_set.filter(crypto=transaction.crypto).first()
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

        # Send email notifications to users
        for transaction in queryset:
            user = transaction.user
            subject = f"Transaction Failed - {transaction.crypto.symbol}"
            message = (
                f"Dear {user.get_full_name},\n\n"
                f"We regret to inform you that your transaction with the following details has failed:\n\n"
                f"Transaction ID: {transaction.transaction_id}\n"
                f"Crypto: {transaction.crypto.name}\n"
                f"Amount: ${transaction.amount}\n"
                f"Plan: {transaction.plan if transaction.plan else 'N/A'}\n\n"
                f"If you have any questions or need further assistance, please contact our support team admin@mywealthwiseinvest.com.\n\n"
                f"Best regards,\n{settings.COMPANY_NAME} Team"
            )

            # Send the email
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=True,
            )
        
        self.message_user(request, "Selected transactions have been marked as failed and users have been notified.")
        # self.message_user(request, "Selected transactions have been marked as failed.")

    @admin.action(description='Approve selected withdrawals')
    def approve_withdrawals(modeladmin, request, queryset):
        """Admin action to approve selected withdrawals."""
        try:
            for transaction in queryset:
                if transaction.transaction_type == Transaction.WITHDRAWAL and transaction.status == Transaction.PENDING:
                    # Update transaction to 'SUCCESS'
                    transaction.status = Transaction.SUCCESS
                    transaction.save()

                    # Deduct the amount from the user's wallet
                    # wallet = transaction.user.get_wallet_for_crypto(transaction.crypto)
                    wallet = Wallet.objects.get(user=transaction.user)
                    if wallet and wallet.balance >= transaction.amount:
                        wallet.balance -= transaction.amount
                        wallet.save()

                        # Notify user about withdrawal approval
                        subject = f"Withdrawal Approved - {transaction.crypto.symbol}"
                        message = (f"Dear {transaction.user.get_full_name},\n\n"
                                f"Your withdrawal of ${transaction.amount} in {transaction.crypto.name} "
                                f"has been approved.\n\n"
                                f"Thank you for using our service.\n\n"
                                f"Best regards,\n{settings.COMPANY_NAME} Team")

                        send_mail(
                            subject,
                            message,
                            settings.DEFAULT_FROM_EMAIL,
                            [transaction.user.email],
                            fail_silently=True,
                        )
            modeladmin.message_user(request, "Selected withdrawals have been approved.")
        
        except Exception as e:
            modeladmin.message_user(request, f"Error while approving withdrawals: {str(e)}", level='error')

    mark_as_confirmed.short_description = "Mark selected transactions as Confirmed"
    mark_as_failed.short_description = "Mark selected transactions as Failed"

admin.site.register(Transaction, TransactionAdmin)


admin.site.register(User)
admin.site.register(Cryptocurrency)
admin.site.register(Wallet)