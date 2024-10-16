from django.urls import path
from .views import InventoryItemListView, InventoryItemDetailView

urlpatterns = [
    path("items/", InventoryItemListView.as_view(), name="inventory_items"),
    path(
        "items/<int:item_id>/",
        InventoryItemDetailView.as_view(),
        name="inventory_item_details",
    ),
]
