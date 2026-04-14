from django.contrib import admin
from .models import Plan


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'plan_type', 'price', 'validity_days', 'is_active', 'created_at')
    list_filter = ('plan_type', 'is_active')
    search_fields = ('name', 'description')
    list_editable = ('is_active',)
