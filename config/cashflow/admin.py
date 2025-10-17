from django.contrib import admin
from .models import CashFlowEntry

@admin.register(CashFlowEntry)
class CashFlowEntryAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'status', 'type', 'category', 'subcategory', 'amount')
    list_filter = ('created_at', 'status', 'type', 'category', 'subcategory')
    search_fields = ('comment',)
