from django.db import models
from django.urls import reverse
from django.template.defaultfilters import slugify

# Create your models here.

class Category(models.Model):
    #Spirit or product category. IE: Whisky, Bourbon etc.
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name 


class Spirit(models.Model):
    #The Bartsbottles item# from the database. This will be used to read items from their DB and compare current stock vs forecasted use.
    item_nr = models.CharField(max_length=10)
    #The spirit or product name
    name = models.CharField(max_length=255)
    #Linked to the category model. This will be used to display the category an item belongs on a template.
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    slug = models.SlugField()

    def __str__(self):
        return self.name 
    
    def save(self, *args, **kwargs):
        self.slug = slugify({self.name})
        super(Spirit, self).save()




class Account(models.Model):
    #Name of the account that will be used to link selected products.
    name = models.CharField(max_length=255)
    slug = models.SlugField()

    def __str__(self):
       return self.name
    
    def get_absolute_url(self):
        return reverse("forecast:account_detail", kwargs={"name": self.name})
    
    def save(self, *args, **kwargs):
        self.slug = slugify({self.name})
        super(Account, self).save()


class VolumeItem(models.Model):
    # The core model that all forecasted volume is build on.
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    spirit = models.ForeignKey(Spirit, on_delete=models.CASCADE)
    #The correct category will be automatically linked wehn the model is saved.
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    #Amount will be used to calculate and display the forecast volume
    amount = models.IntegerField()
    #Forecasted volume will be based on the start and end date.
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