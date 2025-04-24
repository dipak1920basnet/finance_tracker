from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
# Create your models here.

from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    pass

class Category(models.Model):
    name = models.CharField(max_length=256, blank=True, null=True)
    user = models.ForeignKey('User', on_delete=models.CASCADE, null= True, blank=True, related_name="usercat")

    def __str__(self):
        return self.name

class Transaction(models.Model):

    income = 'income'
    expense = 'expense'

    CHOICES = [

        (income,"Income"),
        (expense, "Expense")
    ]

    user = models.ForeignKey('User', on_delete=models.CASCADE)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    amount = models.IntegerField()
    date = models.DateTimeField()
    description = models.CharField(max_length=500)
    type = models.CharField(
        max_length=10,
        choices=CHOICES,
        default=income)
    
    def __str__(self):
         return f"{self.type.capitalize()} - ${self.amount} on {self.date.date()}"

class Budget(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    month = models.IntegerField(
        validators=[
            MinValueValidator(1),
            # Get the month within range of 1 to 12
            MaxValueValidator(12)
        ]
    )
    amount = models.IntegerField()
