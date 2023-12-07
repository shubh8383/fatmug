
from django.utils import timezone
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status

from .models import HistoricalPerformance, Vendor, PurchaseOrder
from .serializers import VendorSerializer, PurchaseOrderSerializer, VendorPerformanceSerializer

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000


class VendorListCreateView(generics.ListCreateAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    pagination_class = StandardResultsSetPagination


class VendorDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    

class PurchaseOrderListCreateView(generics.ListCreateAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer
    pagination_class = StandardResultsSetPagination

class PurchaseOrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer

class VendorPerformanceView(generics.RetrieveAPIView):
    queryset = HistoricalPerformance.objects.all()
    serializer_class = VendorPerformanceSerializer

    # def retrieve(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     performance_data = {
    #         'on_time_delivery_rate': instance.on_time_delivery_rate,
    #         'quality_rating': instance.quality_rating_avg,
    #         'response_time': instance.average_response_time,
    #         'fulfilment_rate': instance.fulfillment_rate
    #     }
    #     return Response(performance_data, status=status.HTTP_200_OK)
    
    
    
class AcknowledgePurchaseOrderView(generics.CreateAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer

    def create(self, request, *args, **kwargs):
        instance = self.get_object()
        
        if instance.acknowledgment_date is not None:
            return Response({"error": "Purchase order already acknowledged"}, status=status.HTTP_400_BAD_REQUEST)

        instance.acknowledgment_date = timezone.now()
        instance.save()

        vendor = instance.vendor
        vendor.calculate_performance_metrics()

        return Response({"message": "Purchase order acknowledged successfully"}, status=status.HTTP_200_OK)