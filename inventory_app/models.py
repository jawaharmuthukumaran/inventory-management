from django.db import models
from django.core.validators import RegexValidator

# Create your models here.


class InventoryItem(models.Model):
    item_name = models.CharField(max_length=100)
    item_code = models.CharField(
        max_length=100,
        unique=True,
        validators=[
            RegexValidator(
                regex=r"^[A-Za-z0-9_]+$",  # Alphanumeric and underscores only
                message="Item code must be alphanumeric, and can include underscores only.",
                code="invalid_item_code",
            )
        ],
    )
    description = models.TextField()
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.item_name

    def clean(self):
        # Convert item_code to lowercase before saving
        self.item_code = self.item_code.lower()

    def save(self, *args, **kwargs):
        # Call clean() to apply lowercase conversion
        self.clean()
        super().save(*args, **kwargs)
