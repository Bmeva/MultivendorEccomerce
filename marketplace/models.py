from django.db import models
from accounts.models import User
from Menu.models import fooditem



# Create your models here.

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fooditem = models.ForeignKey(fooditem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.user #user is a foreign key thats why we defined it as unicode
    
class Tax(models.Model):
    tax_type = models.CharField(max_length=100, unique=True)
    tax_percentage = models.DecimalField(decimal_places=2, max_digits=4, verbose_name="Tax Percentage (%)")#the verboase name would replace the name of the lable on the admin panel
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = 'Tax' #without this on the admin panel Tax field would display as Taxs

    def __str__(self):
        return self.tax_type