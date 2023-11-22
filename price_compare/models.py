from django.db import models

# Create your models here.
class Tracked_Products(models.Model):
    link = models.URLField()
    name = models.CharField(max_length=255)
    supplier = models.CharField(max_length=255)
    price = models.CharField(max_length=50)
    previous_price = models.CharField(max_length=50, blank=True, null=True)
    start_tracking_date = models.DateField(auto_now_add=True)
    start_price_change_date = models.DateField(auto_now=True)


    def __str__(self):
        return (f"{self.name} at {self.supplier}")

