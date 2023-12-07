from django.db import models
from django.db.models import Count, Avg, F
from django.utils import timezone

# Create your models here.

class Vendor(models.Model):
    name = models.CharField(max_length=255)
    contact_details = models.TextField()
    address = models.TextField()
    vendor_code = models.CharField(max_length=50, unique=True)
    on_time_delivery_rate = models.FloatField(default=0)
    quality_rating_avg = models.FloatField(default=0)
    average_response_time = models.FloatField(default=0)
    fulfillment_rate = models.FloatField(default=0)
    
    class Meta:
        indexes = [
            models.Index(fields=['name'])
        ]

    def __str__(self):
        return self.name
    
    def calculate_performance_metrics(self):
        completed_pos = self.purchase_orders.filter(status='completed')
        
        on_time_delivery_rate = completed_pos.filter(delivery_date__lte=F('acknowledgment_date')).count() / completed_pos.count() * 100 if completed_pos.count() > 0 else 0

        quality_rating_avg = completed_pos.aggregate(avg_quality=Avg('quality_rating'))['avg_quality'] if completed_pos.count() > 0 else 0

        avg_response_time = completed_pos.exclude(acknowledgment_date__isnull=True).aggregate(
            avg_time=Avg(F('acknowledgment_date') - F('issue_date')))['avg_time']
        
        avg_response_time_seconds = avg_response_time.total_seconds() if avg_response_time else 0
        
        fulfillment_rate = completed_pos.filter(status='completed').count() / self.purchase_orders.count() * 100 if self.purchase_orders.count() > 0 else 0

        
        self.on_time_delivery_rate = on_time_delivery_rate
        self.quality_rating_avg = quality_rating_avg
        self.average_response_time = avg_response_time_seconds
        self.fulfillment_rate = fulfillment_rate
        self.save()



class PurchaseOrder(models.Model):
    po_number = models.CharField(max_length=50, unique=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name="purchase_orders")
    order_date = models.DateTimeField()
    delivery_date = models.DateTimeField()
    items = models.JSONField()
    quantity = models.IntegerField()
    status = models.CharField(max_length=50)
    quality_rating = models.FloatField(null=True, blank=True)
    issue_date = models.DateTimeField()
    acknowledgment_date = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['vendor', 'order_date'])
        ]

    def __str__(self):
        return f"PO {self.po_number} - {self.vendor.name}"



class HistoricalPerformance(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name="historical_performances")
    date = models.DateTimeField()
    on_time_delivery_rate = models.FloatField()
    quality_rating_avg = models.FloatField()
    average_response_time = models.FloatField()
    fulfillment_rate = models.FloatField()
    
    class Meta:
        indexes = [
            models.Index(fields=['vendor', 'date'])
        ]

    def __str__(self):
        return f"{self.vendor.name} - {self.date}"
    
    
    def create_performance_metrics(vendor):
        completed_pos = vendor.purchase_orders.filter(status='completed')
        
        on_time_delivery_rate = completed_pos.filter(delivery_date__lte=F('acknowledgment_date')).count() / completed_pos.count() * 100 if completed_pos.count() > 0 else 0

        quality_rating_avg = completed_pos.aggregate(avg_quality=Avg('quality_rating'))['avg_quality'] if completed_pos.count() > 0 else 0

        avg_response_time = completed_pos.exclude(acknowledgment_date__isnull=True).aggregate(
            avg_time=Avg(F('acknowledgment_date') - F('issue_date')))['avg_time']
        
        avg_response_time_seconds = avg_response_time.total_seconds() if avg_response_time else 0
        
        fulfillment_rate = completed_pos.filter(status='completed').count() / vendor.purchase_orders.count() * 100 if vendor.purchase_orders.count() > 0 else 0

        HistoricalPerformance.objects.create(vendor = vendor,date = timezone.now(),
        on_time_delivery_rate = on_time_delivery_rate,
        quality_rating_avg = quality_rating_avg,
        average_response_time = avg_response_time_seconds,
        fulfillment_rate = fulfillment_rate)


    def calculate_performance_metrics(self):
        completed_pos = self.vendor.purchase_orders.filter(status='completed')
        
        on_time_delivery_rate = completed_pos.filter(delivery_date__lte=F('acknowledgment_date')).count() / completed_pos.count() * 100 if completed_pos.count() > 0 else 0

        quality_rating_avg = completed_pos.aggregate(avg_quality=Avg('quality_rating'))['avg_quality'] if completed_pos.count() > 0 else 0

        avg_response_time = completed_pos.exclude(acknowledgment_date__isnull=True).aggregate(
            avg_time=Avg(F('acknowledgment_date') - F('issue_date')))['avg_time']
        
        avg_response_time_seconds = avg_response_time.total_seconds() if avg_response_time else 0
        
        fulfillment_rate = completed_pos.filter(status='completed').count() / self.purchase_orders.count() * 100 if self.purchase_orders.count() > 0 else 0

        self.date = timezone.now()
        self.on_time_delivery_rate = on_time_delivery_rate
        self.quality_rating_avg = quality_rating_avg
        self.average_response_time = avg_response_time_seconds
        self.fulfillment_rate = fulfillment_rate
        self.save()