from django.contrib import admin
from .models import Vendor, PurchaseOrder, HistoricalPerformance

class PurchaseOrderInline(admin.TabularInline):
    model = PurchaseOrder
    extra = 0

class HistoricalPerformanceInline(admin.TabularInline):
    model = HistoricalPerformance
    extra = 0

@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ('name', 'vendor_code', 'on_time_delivery_rate', 'quality_rating_avg', 'average_response_time', 'fulfillment_rate')
    search_fields = ('name', 'vendor_code')
    inlines = [PurchaseOrderInline, HistoricalPerformanceInline]

@admin.register(PurchaseOrder)
class PurchaseOrderAdmin(admin.ModelAdmin):
    list_display = ('po_number', 'vendor', 'order_date', 'delivery_date', 'status', 'quality_rating', 'acknowledgment_date')
    search_fields = ('po_number', 'vendor__name')
    list_filter = ('status', 'acknowledgment_date')
    date_hierarchy = 'order_date'

@admin.register(HistoricalPerformance)
class HistoricalPerformanceAdmin(admin.ModelAdmin):
    list_display = ('vendor', 'date', 'on_time_delivery_rate', 'quality_rating_avg', 'average_response_time', 'fulfillment_rate')
    search_fields = ('vendor__name',)
    list_filter = ('vendor', 'date')
    date_hierarchy = 'date'
