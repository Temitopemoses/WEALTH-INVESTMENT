from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Cryptocurrency, Transaction, Wallet

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
        queryset.update(status='SUCCESS')
        for transaction in queryset:
            if transaction.status == 'SUCCESS':
                transaction.user.wallet_balance += transaction.amount
                transaction.user.save()
        self.message_user(request, "Selected transactions have been marked as confirmed.")


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