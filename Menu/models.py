from django.db import models

from vendor.models import vendor
# Create your models here.




# Create your models here.

class Category(models.Model):
    Vendor = models.ForeignKey(vendor, on_delete=models.CASCADE) #if the vendor is deleted all associated categories should also be deleted. 
    #becouse of the vendor model we called while creating a category it would show all vendors in a drop down
    category_name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=100, unique=True) #It  would create a friendly url of the category. 
    #so if the category is sea food then the slug would be sea-food
    description = models.TextField(max_length=250, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta: # without this code my model name would be Categorys
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
    
    def clean(self):
        self.category_name = self.category_name.capitalize()
        #we made this function so that the user cannot create the same category name in small and capital letters

    def __str__(self):
        return self.category_name
    
class fooditem(models.Model):
    vendor = models.ForeignKey(vendor, on_delete=models.CASCADE) #the vendor is calling venvor model on the vendor app
     #becouse of the vendor model we called while creating a category it would show all vendors in a drop down
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='fooditems') #category is calling the Category model above
     #becouse of the Category model we called while creating a fooditem it would show all categories in a drop down
    food_title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True) # if you want it to have a default value then use default='my-food'
    description = models.TextField(max_length=250, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='foodimages')
    is_available = models.BooleanField(default=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.food_title

