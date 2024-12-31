from django.db import models


class Book(models.Model):
    COVER_TYPE_CHOICES = [
        ("HARD", "Hard Cover"),
        ("SOFT", "Soft Cover"),
    ]

    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    cover = models.CharField(max_length=10, choices=COVER_TYPE_CHOICES)
    inventory = models.PositiveIntegerField(default=0)
    daily_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    def __str__(self):
        return f"book id: {self.id}, '{self.title}', (inventory : {self.inventory})"

    def save(self, *args, **kwargs):
        if self.inventory < 0:
            raise ValueError("Inventory cannot be negative")
        super().save(*args, **kwargs)
