from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import InventoryItemSerializer
from .models import InventoryItem
from django.core.cache import cache
import logging

# Set up a logger for this module
logger = logging.getLogger(__name__)


class InventoryItemListView(APIView):

    def get(self, request):
        cache_key = "all_inventory_items"  # Define a cache key for the items list
        cached_items = cache.get(cache_key)

        # If items are found in the cache, return them directly
        if cached_items:
            logger.info("Returning cached items list")
            return Response(cached_items, status=status.HTTP_200_OK)

        # Attempt to retrieve all items from the database
        items = InventoryItem.objects.all()

        # Check if there are no items and log accordingly
        if not items.exists():
            logger.info("No items found in the inventory")
            return Response({"message": "No items found"}, status=status.HTTP_200_OK)

        # Serialize the items
        serializer = InventoryItemSerializer(items, many=True)

        # Cache the serialized data for 5 minutes
        cache.set(cache_key, serializer.data, timeout=300)  # Cache for 5 minutes
        logger.info("Items list cached successfully")

        # Return the serialized data
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):

        # Deserialize the request data
        serializer = InventoryItemSerializer(data=request.data)

        # Check if an item with the same item_code already exists
        item_code = request.data.get("item_code")
        if InventoryItem.objects.filter(item_code=item_code).exists():
            logger.warning("Item with item_code '%s' already exists", item_code)
            return Response(
                {"error": "Item already exists"}, status=status.HTTP_400_BAD_REQUEST
            )

        # Validate and save the new item if no such item exists
        if serializer.is_valid():
            item = serializer.save()  # Save the new item to the database

            # Clear cache after creating a new item
            cache.delete("all_inventory_items")
            logger.info("Cache cleared after creating a new item with id %s", item.id)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        logger.warning("Validation errors on item creation: %s", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class InventoryItemDetailView(APIView):

    def get(self, request, item_id):
        cache_key = f"inventory_item_{item_id}"

        # Try to retrieve the item from cache
        cached_item = cache.get(cache_key)
        if cached_item:
            logger.info("Retrieved item %s from cache", item_id)
            return Response(cached_item, status=status.HTTP_200_OK)

        # Retrieve item from database if not cached
        inventory_item = get_object_or_404(InventoryItem, pk=item_id)
        serializer = InventoryItemSerializer(inventory_item)
        serialized_data = serializer.data

        # Cache the serialized data for future requests
        cache.set(cache_key, serialized_data, timeout=300)
        logger.info("Item %s cached", item_id)

        # Return the serialized data
        return Response(serialized_data, status=status.HTTP_200_OK)

    def put(self, request, item_id):
        cache_key = f"inventory_item_{item_id}"

        # Retrieve the item from the database
        inventory_item = get_object_or_404(InventoryItem, pk=item_id)
        serializer = InventoryItemSerializer(inventory_item, data=request.data)

        # Validate and save updated data
        if serializer.is_valid():
            serializer.save()

            # Cache the updated data for future GET requests
            cache.set(cache_key, serializer.data, timeout=300)
            logger.info("Updated item %s and refreshed cache", item_id)

            return Response(serializer.data, status=status.HTTP_200_OK)

        logger.warning("Validation errors on PUT request: %s", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, item_id):
        cache_key = f"inventory_item_{item_id}"

        # Retrieve the item from the database
        inventory_item = get_object_or_404(InventoryItem, pk=item_id)

        # Delete the item and clear it from cache
        inventory_item.delete()
        cache.delete(cache_key)
        logger.info("Deleted item %s and cleared cache", item_id)

        return Response(
            {"message": "Item deleted Successfully"}, status=status.HTTP_200_OK
        )
