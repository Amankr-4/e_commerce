from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator , MinValueValidator
# Create your models here.

# python tuple
STATE_CHOICES  = (
    ('bihar','bihar'),
    ('jharkhand','jharkhand'),
    ('kashmir','kashmir')
)

class customer (models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=200)  #in CharField specifying length is must
    locality = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    zipcode = models.IntegerField()
    state = models.CharField(choices=STATE_CHOICES,max_length=50)
    def __str__(self):
        return str(self.id) #self.id ek integer dega but ye func. string return karta h  so str(self.id) se typecast kiye h string value me

CATEGORY_CHOICES = (('M' , 'Mobile'),
            ('L','Laptop'),
            ('TW','top wear'),
            ('BW','Bottom wear'),
            )

class product (models.Model):
    title = models.CharField(max_length=200)
    selling_price = models.FloatField()
    discounted_price = models.FloatField()
    description = models.TextField()
    brand = models.CharField(max_length=200)
    category = models.CharField(choices=CATEGORY_CHOICES,max_length=2)
    product_image = models.ImageField(upload_to='productimg')
    def __str__(self):
        return str(self.id)
    
class cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product =models.ForeignKey(product , on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    def __str__(self):
        return str(self.id)
    
    @property   #this is used to show the the cost of each items in the checkout page
    def total_cost(self):
        return self.quantity*self.product.discounted_price
    

    
STATUS_CHOICES = (
    ('Accepted','Accepted'),
    ('packed','packed'),
    ('on the way','on the way'),
    ('delivered','delivered'),
    ('Cancel','Cancel')
)

class orderPlaced(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    customer = models.ForeignKey(customer,on_delete=models.CASCADE)
    product = models.ForeignKey(product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default = 1)
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=STATUS_CHOICES,max_length=40,default='pending')
    @property   #this is used to show the the cost of each items in the checkout page
    def total_cost(self):
        return self.quantity*self.product.discounted_price
   
    
    
    
    