from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Register your models here.

from .models import Agency, Bank, Category, CategoryValue, Indicator, IndAgency, Locality, UserAgency, User

# class UserProfileInline(admin.StackedInline):
#     can_delete = False


admin.site.register(Agency)
admin.site.register(Bank)
admin.site.register(Category)
admin.site.register(CategoryValue)
admin.site.register(Indicator)
admin.site.register(IndAgency)
admin.site.register(Locality)
admin.site.register(UserAgency)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': (
            'first_name', 'last_name', 'dob', "address", 'phone', 'code', 'post')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'first_name', 'last_name',
                    'is_staff', 'dob', "address", 'phone', 'code', 'post')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
    # inlines = (UserProfileInline, )
