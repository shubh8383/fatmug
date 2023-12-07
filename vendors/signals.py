
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import PurchaseOrder, HistoricalPerformance


@receiver(post_save, sender=PurchaseOrder)
def update_vendor_performance(sender, instance, **kwargs):
    if instance.vendor:
        instance.vendor.calculate_performance_metrics()
        history = HistoricalPerformance.objects.filter(vendor_id = instance.vendor.id)
        if history.exists():
            history.first().calculate_performance_metrics()
        else:
            HistoricalPerformance.create_performance_metrics(vendor=instance.vendor)
        