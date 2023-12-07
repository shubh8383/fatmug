# urls.py

from django.urls import path
import vendors.views as vendors_views

urlpatterns = [
    path('vendors/', vendors_views.VendorListCreateView.as_view(), name='vendor-list-create'),
    path('vendors/<int:pk>/', vendors_views.VendorDetailView.as_view(), name='vendor-detail'),
    path('purchase_orders/', vendors_views.PurchaseOrderListCreateView.as_view(), name='purchase-order-list-create'),
    path('purchase_orders/<int:pk>/', vendors_views.PurchaseOrderDetailView.as_view(), name='purchase-order-detail'),
    path('vendors/<int:pk>/performance/', vendors_views.VendorPerformanceView.as_view(), name='vendor-performance'),
    path('purchase_orders/<int:pk>/acknowledge/', vendors_views.AcknowledgePurchaseOrderView.as_view(), name='acknowledge-purchase-order'),
]
