from django.shortcuts import render,HttpResponseRedirect ,redirect
from django.views import View
from .models import *
from .forms import *
from django.contrib import messages
from django.contrib.auth import logout
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required  # for function based view which should only be seen when a user is logged in
from django.utils.decorators import method_decorator       # for class based view which should only be seen when a user is logged in


class productview(View):
    def get(self,request):
        topwears = product.objects.filter(category = 'TW')
        bottomwears = product.objects.filter(category = 'BW')
        mobiles = product.objects.filter(category = 'M')
        return render(request,'app/home.html',{'topwears' : topwears,'bottomwears':bottomwears,'mobiles':mobiles})

# def product_detail(request):
#  return render(request, 'app/productdetail.html')

class productdetails(View):
    def get(self,request,pk):
        Product = product.objects.get(pk = pk)
        if request.user.is_authenticated:
            item_already_exist_in_cart = False
            item_already_exist_in_cart = cart.objects.get(Q(product = Product.id)&Q(user=request.user)).exists()
            return render(request,'app/productdetail.html',{'product':Product,'item_already_exist_in_cart':item_already_exist_in_cart})
        return redirect('/accounts/login')

# to add products in cart model
def add_to_cart(request):
    usr = request.user
    product_id = request.GET.get('prod_id')
    Product = product.objects.get(id =product_id)
    cart(product = Product,user = usr).save()
    return redirect('/cart')

# to show the cart table of logged in user
@login_required
def show_cart(request):
    if request.user.is_authenticated:
        user = request.user
        Cart = cart.objects.filter(user=user)  # Cart is query set of cart table objects having user is current user
        amount =0.0
        shipping_amount = 70.0
        total_amount = 0.0
        if Cart :
            for p in Cart:
                tempamount = (p.quantity*p.product.discounted_price)
                amount+=tempamount
            total_amount = amount + shipping_amount    
            return render(request,'app/addtocart.html',{'carts':Cart,'amount' : amount , 'total_amount' : total_amount})
        else:
            return render(request,'app/emptycart.html')


def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = cart.objects.get(Q(product=prod_id)&Q(user=request.user))
        c.quantity+=1
        c.save()
        amount = 0.0
        shipping_amount = 70.0
        total_amount=0.0
        user = request.user
        Cart = cart.objects.filter(user=user)
        for p in Cart:
            tempamount = (p.quantity*p.product.discounted_price)
            amount+=tempamount
        total_amount = amount + shipping_amount 
        
    data = {
        'quantity' : c.quantity,
        'amount' : amount,
        'totalamount' : total_amount
    }
    return JsonResponse(data)
      
      
def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = cart.objects.get(Q(product=prod_id)&Q(user=request.user))
        c.quantity-=1
        c.save()
        amount = 0.0
        shipping_amount = 70.0
        total_amount=0.0
        user = request.user
        Cart = cart.objects.filter(user=user)
        for p in Cart:
            tempamount = (p.quantity*p.product.discounted_price)
            amount+=tempamount
        total_amount = amount + shipping_amount 
        
    data = {
        'quantity' : c.quantity,
        'amount' : amount,
        'totalamount' : total_amount
    }
    return JsonResponse(data)  

@login_required
def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = cart.objects.get(Q(product=prod_id)&Q(user=request.user))
        c.delete()
        amount = 0.0
        shipping_amount = 70.0
        total_amount=0.0
        user = request.user
        Cart = cart.objects.filter(user=user)
        for p in Cart:
            tempamount = (p.quantity*p.product.discounted_price)
            amount+=tempamount
        total_amount = amount + shipping_amount 
        
    data = {
        'amount' : amount,
        'totalamount' : total_amount
    }
    return JsonResponse(data)  


def buy_now(request):
 return render(request, 'app/buynow.html')


@method_decorator(login_required,name='dispatch')
class ProfileView(View):
    def get(self,request):
        form = CustomerProfileForm()
        return render(request,'app/profile.html',{'form':form,'active':'btn-primary'})
    def post(self,request):
        form  = CustomerProfileForm(request.POST)
        if form.is_valid():
            usr = request.user  # isse hume current logged in ka user name mil jata h
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            reg = customer(user=usr,name= name, locality = locality,city = city,state = state , zipcode = zipcode)
            reg.save()
            messages.success(request,'Congratulations!! Profile Updated Successfully :)')
        return render(request, 'app/profile.html',{'form':form,'active':'btn-primary'})        
    
     
def address(request):
    addresses = customer.objects.filter(user = request.user) 
    return render(request, 'app/address.html',{'addresses':addresses,'active':'btn-primary'})

@login_required
def orders(request):
    op = orderPlaced.objects.filter(user = request.user)
    return render(request, 'app/orders.html',{'orderplaced':op})



def mobile(request,data=None):
    if data == None:
        mobiles = product.objects.filter(category='M')
    elif data == 'oppo' or data == 'Apple':
        mobiles = product.objects.filter(category = 'M').filter(brand=data) 
    elif data == 'below':
        mobiles = product.objects.filter(category = 'M').filter(discounted_price__lt = 15000) 
    elif data == 'above':                                      #yaha ye __lt mltb less then 15000 wala filter kardega similarly __gt greater then
        mobiles = product.objects.filter(category = 'M').filter(discounted_price__gt = 15000)
    return render(request, 'app/mobile.html',{'mobiles':mobiles})  

     
class customerRegistration(View):
    def get(self,request):  # get request h to blank form dikha
        form = customerRegistrationForm()
        return render(request, 'app/customerregistration.html',{'form':form})
    def post(self,request):  # post request h to filled data  check karke save karde aur form dikha
        form = customerRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request,'Congratulations!! Registrated Successfully :)')
            form.save()
        return render(request, 'app/customerregistration.html',{'form':form})        

@login_required
def checkout(request):
    user= request.user
    address = customer.objects.filter(user=user) 
    cart_items = cart.objects.filter(user=user)
    amount =0.0
    shipping_amount = 70.0
    total_amount =0.0
    user = request.user
    Cart = cart.objects.filter(user=user)
    if Cart:
        for p in Cart:
            tempamount = (p.quantity*p.product.discounted_price)
            amount+=tempamount
        total_amount = amount + shipping_amount 
    return render(request, 'app/checkout.html',{'addresses':address,'total_amount':total_amount,'cart_items':cart_items})

def payment_done(request):
    user = request.user
    custid =request.GET.get('custid')  # we are getting it from the checkout.html page in form there is action associated with it that whenever we click on radio btn we get the customer id 
    Customer = customer.objects.get(id = custid)
    Cart = cart.objects.filter(user=user)
    for c in Cart:
        orderPlaced(user=user,customer= Customer,product = c.product,quantity=c.quantity).save()
        c.delete()
    return redirect('/orders')

def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/accounts/login/')

