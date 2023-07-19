from django.contrib import admin
# from .models import User , customer , product , orderPlaced , cart
from .models import *
# Register your models here.

# admin.site.register(User)  // isse nhi karna h ye hume builtin mila tha

# shortcut way to register

# admin.site.register(customer)
# admin.site.register(product)
# admin.site.register(orderPlaced)
# admin.site.register(cart)

# more detailed way to register

@admin.register(customer)
class customeradmin(admin.ModelAdmin):
    list_display = ('id','user','name','locality','city','zipcode','state')
@admin.register(product)
class productadmin(admin.ModelAdmin):
    list_display = ('id','title','selling_price','discounted_price','description','brand','category','product_image')
    
@admin.register(orderPlaced)
class orderPlacedadmin(admin.ModelAdmin):
    list_display = ('id','user','customer','product','quantity','order_date','status')
@admin.register(cart)
class cartadmin(admin.ModelAdmin):
    list_display = ('id','user','product','quantity')

