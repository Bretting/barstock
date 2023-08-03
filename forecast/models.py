from django.db import models
from django.db.models import Sum
from django.urls import reverse

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name 


class Spirit(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name 


class Account(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
       return self.name
    
    def get_absolute_url(self):
        return reverse("forecast:account_detail", kwargs={"id": self.pk})


class VolumeItem(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    spirit = models.ForeignKey(Spirit, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    amount = models.IntegerField()
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)


    def get_account_url(self):
        return reverse("forecast:account_detail", kwargs={"pk": self.account.pk})
   
    def __str__(self):
        return f"{self.account}, {self.spirit} - {self.amount}"
    
    def save(self, *args, **kwargs):
        # If the VolumeItem object doesn't have a category assigned, get it from the related Spirits object
        if not self.category:
            self.category = self.spirit.category
        super().save(*args, **kwargs)