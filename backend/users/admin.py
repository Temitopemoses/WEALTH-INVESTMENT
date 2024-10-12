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
admin.site.register(User)
admin.site.register(Cryptocurrency)
admin.site.register(Transaction)
admin.site.register(Wallet)