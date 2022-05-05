from django.shortcuts import render,redirect
from .models import Contact,User,Product,Wishlist,Cart,Transaction,Order
from django.utils import timezone
from django.conf import settings
from myapp.templates.paytm import generate_checksum, verify_checksum

from django.views.decorators.csrf import csrf_exempt


# Create your views here.
def initiate_payment(request):
    user=User.objects.get(email=request.session['email'])
    if request.method=="POST":
        try:
            amount = int(request.POST['amount'])
        except:
            return render(request, 'pay.html', context={'error': 'Wrong Accound Details or amount'})

        transaction = Transaction.objects.create(made_by=user,amount=amount)
        transaction.save()

        cart=Cart.objects.filter(user=user)
        for i in cart:
            i.payment_status="paid"
            i.date=timezone.now()
            i.save()
        cart=Cart.objects.filter(user=user,payment_status="pending")
        request.session['cart_count']=len(cart)
        merchant_key = settings.PAYTM_SECRET_KEY

        params = (
            ('MID', settings.PAYTM_MERCHANT_ID),
            ('ORDER_ID', str(transaction.order_id)),
            ('CUST_ID', str(transaction.made_by.email)),
            ('TXN_AMOUNT', str(transaction.amount)),
            ('CHANNEL_ID', settings.PAYTM_CHANNEL_ID),
            ('WEBSITE', settings.PAYTM_WEBSITE),
            # ('EMAIL', request.user.email),
            # ('MOBILE_N0', '9911223388'),
            ('INDUSTRY_TYPE_ID', settings.PAYTM_INDUSTRY_TYPE_ID),
            ('CALLBACK_URL', 'http://localhost:8000/callback/'),
            # ('PAYMENT_MODE_ONLY', 'NO'),
        )

        paytm_params = dict(params)
        checksum = generate_checksum(paytm_params, merchant_key)

        transaction.checksum = checksum
        transaction.save()

        paytm_params['CHECKSUMHASH'] = checksum
        print('SENT: ', checksum)

    Order.objects.create(
        fname=request.POST['fname'],
        lname=request.POST['lname'],
        state=request.POST['state'],
        street_address1=request.POST['street_address1'],
        street_address2=request.POST['street_address2'],
        city=request.POST['city'],
        postcode=request.POST['postcode'],
        mobile=request.POST['mobile'],
        email=request.POST['email']
    )
    return render(request, 'redirect.html', context=paytm_params)


@csrf_exempt
def callback(request):
    if request.method == 'POST':
        received_data = dict(request.POST)
        paytm_params = {}
        paytm_checksum = received_data['CHECKSUMHASH'][0]
        for key, value in received_data.items():
            if key == 'CHECKSUMHASH':
                paytm_checksum = value[0]
            else:
                paytm_params[key] = str(value[0])
        # Verify checksum
        is_valid_checksum = verify_checksum(paytm_params, settings.PAYTM_SECRET_KEY, str(paytm_checksum))
        if is_valid_checksum:
            received_data['message'] = "Checksum Matched"
        else:
            received_data['message'] = "Checksum Mismatched"
            return render(request, 'callback.html', context=received_data)
        return render(request, 'callback.html', context=received_data)

def index(request):
    try:
        user=User.objects.get(email=request.session['email'])
        products=Product.objects.all()
        if user.usertype=='user':
            return render(request,'index.html',{'products':products})
        else:
            return render(request,'seller_index.html')
    except:
        products=Product.objects.all()
        return render(request,'index.html',{'products':products})

def about(request):
    return render(request,'about.html') 

def cart(request):
    return render(request,'cart.html')

def shop(request):
    products=Product.objects.all()
    garden=len(Product.objects.filter(product_category="garden"))
    plant=len(Product.objects.filter(product_category="plant"))
    seed=len(Product.objects.filter(product_category="seed"))
    fertilizer=len(Product.objects.filter(product_category="fertilizer"))
    accessories=len(Product.objects.filter(product_category="accessories"))
    return render(request,'shop.html',{'products':products,'garden':garden,'plant':plant,'seed':seed,'fertilizer':fertilizer,'accessories':accessories})

def category_garden(request):
    products=Product.objects.filter(product_category="garden")
    garden=len(Product.objects.filter(product_category="garden"))
    plant=len(Product.objects.filter(product_category="plant"))
    seed=len(Product.objects.filter(product_category="seed"))
    fertilizer=len(Product.objects.filter(product_category="fertilizer"))
    accessories=len(Product.objects.filter(product_category="accessories"))
    return render(request,'shop.html',{'products':products,'garden':garden,'plant':plant,'seed':seed,'fertilizer':fertilizer,'accessories':accessories})

def category_plant(request):
    products=Product.objects.filter(product_category="plant")
    garden=len(Product.objects.filter(product_category="garden"))
    plant=len(Product.objects.filter(product_category="plant"))
    seed=len(Product.objects.filter(product_category="seed"))
    fertilizer=len(Product.objects.filter(product_category="fertilizer"))
    accessories=len(Product.objects.filter(product_category="accessories"))
    return render(request,'shop.html',{'products':products,'garden':garden,'plant':plant,'seed':seed,'fertilizer':fertilizer,'accessories':accessories})

def category_seed(request):
    products=Product.objects.filter(product_category="seed")
    garden=len(Product.objects.filter(product_category="garden"))
    plant=len(Product.objects.filter(product_category="plant"))
    seed=len(Product.objects.filter(product_category="seed"))
    fertilizer=len(Product.objects.filter(product_category="fertilizer"))
    accessories=len(Product.objects.filter(product_category="accessories"))
    return render(request,'shop.html',{'products':products,'garden':garden,'plant':plant,'seed':seed,'fertilizer':fertilizer,'accessories':accessories})

def category_fertilizer(request):
    products=Product.objects.filter(product_category="fertilizer")
    garden=len(Product.objects.filter(product_category="garden"))
    plant=len(Product.objects.filter(product_category="plant"))
    seed=len(Product.objects.filter(product_category="seed"))
    fertilizer=len(Product.objects.filter(product_category="fertilizer"))
    accessories=len(Product.objects.filter(product_category="accessories"))
    return render(request,'shop.html',{'products':products,'garden':garden,'plant':plant,'seed':seed,'fertilizer':fertilizer,'accessories':accessories})

def category_accessories(request):
    products=Product.objects.filter(product_category="accessories")
    garden=len(Product.objects.filter(product_category="garden"))
    plant=len(Product.objects.filter(product_category="plant"))
    seed=len(Product.objects.filter(product_category="seed"))
    fertilizer=len(Product.objects.filter(product_category="fertilizer"))
    accessories=len(Product.objects.filter(product_category="accessories"))
    return render(request,'shop.html',{'products':products,'garden':garden,'plant':plant,'seed':seed,'fertilizer':fertilizer,'accessories':accessories})

def contact(request):
    if request.method=="POST":
        Contact.objects.create(
                fname=request.POST['fname'],
                lname=request.POST['lname'],
                email=request.POST['email'],
                subject=request.POST['subject'],
                message=request.POST['message'],
            )
        msg="Contact Saved Successfully"
        return render(request,'contact.html',{'msg':msg})
    else:   
        return render(request,'contact.html')

def shop_details(request):
    return render(request,'shop_details.html')
        
def checkout(request):
    return render(request,'checkout.html')

def signup(request):
    if request.method=="POST":
        try:
            User.objects.get(email=request.POST['email'])
            msg="Email Already Registered"
            return render(request,'signup.html',{'msg':msg})
        except:
            if request.POST['password']==request.POST['cpassword']:    
                User.objects.create(
                        usertype=request.POST['usertype'],
                        fname=request.POST['fname'],
                        lname=request.POST['lname'],
                        email=request.POST['email'],
                        mobile=request.POST['mobile'],
                        address=request.POST['address'],
                        password=request.POST['password'],
                        
                    )
                msg="User Signup Successfully"
                return render(request,'login.html',{'msg':msg})
            else:  
                msg="Password & Confirm Password Does Not Matched" 
                return render(request,'signup.html')
    else:
        return render(request,'signup.html')    
                  

def login(request):
    if request.method=="POST":
        try:
            user=User.objects.get(
                email=request.POST['email'],
                password=request.POST['password']
                )
            if user.usertype=="user":
                request.session['email']=user.email
                request.session['fname']=user.fname
                wishlists=Wishlist.objects.filter(user=user)
                request.session['wishlist_count']=len(wishlists)
                carts=Cart.objects.filter(user=user)
                request.session['cart_count']=len(carts)
                return render(request,'index.html')
            elif user.usertype=="seller":
                request.session['email']=user.email
                request.session['fname']=user.fname
                return render(request,'seller_index.html')
            else:
                pass

        except:
            msg="Email or Password Is Incorrect"
            return render(request,'login.html',{'msg':msg})
    else:
        return render(request,'login.html')

def logout(request):
        try:
            del request.session['email']
            del request.session['fname']
            return render(request,'login.html')
        except:
            return render(request,'login.html')            

def change_password(request):
    user=User.objects.get(email=request.session['email'])
    if user.usertype=="user":
        if request.method=="POST":
            if user.password==request.POST['old_password']:
                if request.POST['new_password']==request.POST['cnew_password']:
                    user.password=request.POST['new_password']
                    user.save()
                    return redirect('logout')
                else:
                    msg="New &Confirm New Password Does Not Matched"
                    return render(request,'change_password.html',{'msg':msg})
            else:
                msg="Old Password Does Not Matched"
                return render(request,'change_password.html',{'msg':msg})        
        else:
            return render(request,'change_password.html') 
    else:
        if request.method=="POST":
            if user.password==request.POST['old_password']:
                if request.POST['new_password']==request.POST['cnew_password']:
                    user.password=request.POST['new_password']
                    user.save()
                    return redirect('logout')
                else:
                    msg="New &Confirm New Password Does Not Matched"
                    return render(request,'seller_change_password.html',{'msg':msg})
            else:
                msg="Old Password Does Not Matched"
                return render(request,'seller_change_password.html',{'msg':msg})        
        else:
            return render(request,'seller_change_password.html') 
    
def seller_index(request):
    return render(request,'seller_index.html')

def seller_add_product(request):
    if request.method=="POST":
        product_seller=User.objects.get(email=request.session['email'])
        Product.objects.create(
                product_seller=product_seller,
                product_category=request.POST['product_category'],
                garden_category=request.POST['garden_category'],
                plant_category=request.POST['plant_category'],
                product_price=request.POST['product_price'],
                product_name=request.POST['product_name'],
                product_desc=request.POST['product_desc'],
                product_image=request.FILES['product_image'],
                product_maintainance=request.POST['product_maintainance'],
                product_waterschedule=request.POST['product_waterschedule']
            )
        msg="Product Added Successfully"
        return render(request,'seller_add_product.html',{'msg':msg})    
    else:    
        return render(request,'seller_add_product.html')    

def seller_view_product(request):
        product_seller=User.objects.get(email=request.session['email'])
        products=Product.objects.filter(product_seller=product_seller)
        return render(request,'seller_view_product.html',{'products':products})

def seller_edit_product(request,pk):
    product=Product.objects.get(pk=pk)
    if request.method=="POST":
        product.product_category=request.POST['product_category']
        product.product_price=request.POST['product_price']
        product.product_price=request.POST['product_name']
        product.product_desc=request.POST['product_desc']
        try:
            product.product_image=request.FILES['product_image']
        except:
            pass
        product.save()        
        return render(request,'seller_edit_product.html',{'product':product})
    else:
        return render(request,'seller_edit_product.html',{'product':product})

def seller_delete_product(request,pk): 
    product=Product.objects.get(pk=pk)
    product.delete()
    return redirect('seller_view_product')           

def product_detail(request,pk):
    wishlist_flag=False
    cart_flag=False
    product=Product.objects.get(pk=pk)
    user=User.objects.get(email=request.session['email'])
    try:
        Wishlist.objects.get(user=user,product=product)
        wishlist_flag=True
    except:
        pass
    try:
        Cart.objects.get(user=user,product=product,payment_status="pending")
        cart_flag=True
    except:
        pass    
    return render(request,'product_detail.html',{'product':product,'wishlist_flag':wishlist_flag,'cart_flag':cart_flag})

def add_to_wishlist(request,pk):
    product=Product.objects.get(pk=pk)
    user=User.objects.get(email=request.session['email'])
    Wishlist.objects.create(
            user=user,
            product=product
        )
    return redirect('wishlist')

def wishlist(request):
    user=User.objects.get(email=request.session['email'])
    wishlists=Wishlist.objects.filter(user=user)
    request.session['wishlist_count']=len(wishlists)
    return render(request,'wishlist.html',{'wishlists':wishlists}) 


def remove_from_wishlist(request,pk):
    product=Product.objects.get(pk=pk)
    user=User.objects.get(email=request.session['email'])
    wishlist=Wishlist.objects.get(product=product,user=user)
    wishlist.delete()
    return redirect('wishlist')

def add_to_cart(request,pk):
    product=Product.objects.get(pk=pk)
    user=User.objects.get(email=request.session['email'])
    Cart.objects.create(
            user=user,
            product=product,
            product_price=product.product_price,
            product_qty=1,
            total_price=product.product_price     
        )
    return redirect('cart')

def cart(request):
    net_price=0
    user=User.objects.get(email=request.session['email'])
    carts=Cart.objects.filter(user=user,payment_status="pending")
    for i in carts:
        net_price=net_price+i.total_price

    request.session['cart_count']=len(carts)
    return render(request,'cart.html',{'carts':carts,'net_price':net_price})

def remove_from_cart(request,pk):
    product=Product.objects.get(pk=pk)
    user=User.objects.get(email=request.session['email'])
    cart=Cart.objects.get(user=user,product=product,payment_status="pending")
    cart.delete()
    return redirect('cart')

def change_qty(request):
    print("change qty called")
    cart=Cart.objects.get(pk=request.POST['cid'])
    product_qty=int(request.POST['product_qty'])
    print(" Product_qty : ",product_qty)
    cart.product_qty=product_qty
    cart.total_price=cart.product_price*product_qty
    cart.save()
    return redirect('cart')  

def myorders(request):
    user=User.objects.get(email=request.session['email'])
    carts=Cart.objects.filter(user=user,payment_status="paid")
    return render(request,'myorders.html',{'carts':carts})

def billing_details(request):
    amount=request.POST['amount']
    return render(request,'billing_details.html',{'amount':amount})


def forgot_password(request):
    if request.method=='POST':
        try:
            user=User.objects.get(email=request.POST['email'])
        except:
            msg='Email Not Registered'
            return render(request,'forgot_password.html',{'msg':msg})
        otp=random.randint(1000,9999)
        subject = 'OTP For Forgot Password'
        message = 'Hello'+user.fname+'your otp for forgot password is '+str(otp)+'.'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [user.email, ]
        send_mail( subject, message, email_from, recipient_list )
        return render(request,'otp.html',{'otp':otp,'email':request.POST['email']})
    else:
        return render(request,'forgot_password.html')

def verify_otp(request):
    otp=request.POST['otp']
    uotp=request.POST['uotp']
    email=request.POST['email']

    if otp==uotp:
        return render(request,'new_password.html',{'email':email})
    else:
        msg="Invalid OTP"
        return render(request,'otp.html',{'otp':otp,'email':email,'msg':msg})

def new_password(request):
    email=request.POST['email']
    print(email)
    p=request.POST['new_password']
    cp=request.POST['cnew_password']
    if p==cp:
        user=User.objects.get(email=email)
        user.password=p
        user.save()
        msg='Password Changed Successfully'
        return render(request,'login.html',{'msg':msg})
    else:
        msg='New Password And Confirm New Password Not Matched'
        return render(request,'new_password.html',{'msg':msg})

def profile(request):
    try:
        info=User.objects.get(email=request.session['email'])
    except:
        return redirect('index')
    return render(request,'profile.html',{'info':info})

def profile_update(request):
    try:
        info=User.objects.get(email=request.session['email'])
    except:
        pass
    try:
        info.fname=request.POST['fname']
        info.lname=request.POST['lname']
        info.email=request.POST['email']
        info.mobile=request.POST['mobile']
        info.address=request.POST['address']
        info.save()
    except:
        pass
    msg="Profile Updated Successfully"
    return render(request,'profile.html',{'info':info,'msg':msg})

def seller_profile(request):
    try:
        info=User.objects.get(email=request.session['email'])
    except:
        return redirect('index')
    return render(request,'seller_profile.html',{'info':info})

def seller_profile_update(request):
    try:
        info=User.objects.get(email=request.session['email'])
    except:
        pass
    try:
        info.fname=request.POST['fname']
        info.lname=request.POST['lname']
        info.email=request.POST['email']
        info.mobile=request.POST['mobile']
        info.address=request.POST['address']
        info.save()
    except:
        pass
    msg="Profile Updated Successfully"
    return render(request,'seller_profile.html',{'info':info,'msg':msg})
                
def search(request):
    products=Product.objects.filter(product_name__contains=request.POST['search'])
    print(request.POST['search'])
    msg="Search Result For "+"'"+request.POST['search']+"'"
    return render(request,'search.html',{'products':products,'msg':msg})                