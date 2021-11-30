from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.db.models import Count

from mptt.admin import MPTTModelAdmin

from accounts.models import (
    Client,
    AdditionalPhone,
    AdditionalEmail,
    SocialNetwork,
    Url,
    Department,
    ClientToDepartment,
    LegalEntity,
)


class AdditionalPhoneInline(admin.TabularInline):
    model = AdditionalPhone
    extra = 0


class AdditionalEmailInline(admin.TabularInline):
    model = AdditionalEmail
    extra = 0


class SocialNetworkInline(admin.TabularInline):
    model = SocialNetwork
    extra = 0


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    inlines = (
        AdditionalPhoneInline,
        AdditionalEmailInline,
        SocialNetworkInline,
    )
    readonly_fields = (
        'created_at',
        'updated_at',
        'status_changed_at',
    )
    list_filter = (
        'created_at',
        'updated_at',
        'status_changed_at',
    )
    search_fields = (
        'username',
        'phone',
        'first_name',
        'last_name',
        'middle_name',
    )
    list_display = (
        'username',
        'phone',
        'first_name',
        'last_name',
        'middle_name',
        'updated_at',
        'created_at',
    )
    exclude = ('id',)


admin.site.register(Url)


class ClientToDepartmentInline(admin.TabularInline):
    model = ClientToDepartment
    readonly_fields = ('created_at',)
    extra = 0


class DepartmentCustomMPTTModelAdmin(MPTTModelAdmin):
    inlines = (ClientToDepartmentInline,)
    exclude = ('id',)
    list_display = ('name', 'get_number_of_clients')

    def get_number_of_clients(self, obj):
        descendants_clients = obj.get_descendants().aggregate(
            clients_count=Count('clients')
        ).get('clients_count', 0) or 0
        return descendants_clients + obj.clients.count()
    get_number_of_clients.short_description = _('Number of clients')


admin.site.register(Department, DepartmentCustomMPTTModelAdmin)


@admin.register(LegalEntity)
class LegalEntityAdmin(admin.ModelAdmin):
    search_fields = (
        'full_name',
        'short_name',
        'inn',
        'kpp',
    )
    list_display = (
        'full_name',
        'short_name',
        'inn',
        'kpp',
    )
    exclude = ('id',)
