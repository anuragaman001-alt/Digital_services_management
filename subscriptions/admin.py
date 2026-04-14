from django.contrib import admin
from .models import Subscription, Invoice


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'plan', 'status', 'activated_at', 'expires_at')
    list_filter = ('status', 'plan__plan_type')
    search_fields = ('user__username', 'user__email', 'plan__name')
    raw_id_fields = ('user', 'plan')


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('invoice_number', 'subscription', 'amount', 'paid', 'generated_at')
    list_filter = ('paid',)
    search_fields = ('invoice_number', 'subscription__user__username')
    readonly_fields = ('invoice_number', 'generated_at')
