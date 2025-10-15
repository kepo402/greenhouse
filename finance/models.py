from django.db import models

class Room(models.Model):
    number = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return f"Room {self.number}"


class Contribution(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='contributions')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    month = models.CharField(max_length=20)  # e.g., "October 2025"
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.room} - ₦{self.amount} ({self.month})"


class Expense(models.Model):
    description = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date_added = models.DateTimeField(auto_now_add=True)
    month = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.description} - ₦{self.amount}"

