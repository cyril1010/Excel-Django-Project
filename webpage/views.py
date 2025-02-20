from django.shortcuts import render,redirect
from adminapp.models import ProductDB,CategoryDB
from webpage.models import ContactDB,UserDB,OrderDB,CartDB,Newsletter
# from django.contrib.auth.hashers import make_password,check_password
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt




def homepage(request):
    products = ProductDB.objects.all()
    categories = CategoryDB.objects.all()
    userName = request.session.get('Username', 'Guest')
    try:
        user = UserDB.objects.get(username=userName)
        Name = user.name
    except UserDB.DoesNotExist:
        Name = 'Guest'

    cart = CartDB.objects.filter(username=userName)
    x = cart.count()

    return render(request, "home.html", {'products': products, 'categories': categories, 'Name': Name,'x':x})

def all_products(request):
    products = ProductDB.objects.all()
    categories = CategoryDB.objects.all()
    return render(request, "all_products.html", {'products': products, 'categories': categories})

def user_contact_page(request):
    categories = CategoryDB.objects.all()
    return render(request, "contact.html")

def contact_save(request):
    if request.method == "POST":
        na = request.POST.get("name")
        nu = request.POST.get("number")
        em = request.POST.get("email")
        su = request.POST.get("subject")
        me = request.POST.get("message")
        contact = ContactDB(name=na,phone=nu,email=em,subject=su,message=me)
        contact.save()
        return redirect('user_contact_page')

def user_contact_page(request):
    categories = CategoryDB.objects.all()
    return render(request, "contact.html",{'categories': categories})

def filtered_page(request,cat_name):
    products = ProductDB.objects.filter(category=cat_name)
    categories = CategoryDB.objects.all()
    return render(request, "filtered_page.html", {'products': products, 'categories': categories})

def product_page(request,prod_name):
    product = ProductDB.objects.get(name=prod_name)
    category = CategoryDB.objects.all()
    return render(request, "single_product.html", {'product': product, 'category': category})

def user_login_page(request):
    return render(request, "userLoginPage.html")

def userSignup(request):
    if request.method == "POST":
        na = request.POST.get("name")
        un = request.POST.get("username")
        nu = request.POST.get("number")
        em = request.POST.get("email")
        pa = request.POST.get("password")
        # hashed_password = make_password(pa)

        user = UserDB(name=na,username=un,phone=nu,email=em,password=pa)
        user.save()
        return redirect(user_login_page)
    else:
        return redirect(user_login_page)


def userLogin(request):
    if request.method == "POST":
        un = request.POST.get("username")
        pa = request.POST.get("password")
        if UserDB.objects.filter(username=un).exists():
            user = UserDB.objects.filter(username=un).first()
            if user and pa:
                request.session['Username'] = un
                return redirect(homepage)
            else:
                return redirect(user_login_page)
        else:
            return redirect(user_login_page)
    else:
        return redirect(user_login_page)

def userLogout(request):
    del request.session['Username']
    return redirect(user_login_page)


def cart(request):
    sub_total = 0
    shipping_amount = 0
    cart = CartDB.objects.filter(username=request.session['Username'])
    for i in cart:
        sub_total += i.TotalPrice

    if sub_total>1000:
        shipping_amount=100
    else:
        shipping_amount=200
    total_amount = sub_total+shipping_amount

    context = {'cartproducts': cart, 'subtotal': sub_total, 'shippingamount': shipping_amount, 'totalamount': total_amount}
    return render(request,"cart.html", context)

def save_cart(request):
    if request.method == "POST":
        # Get data from POST and handle missing/empty values
        product_name = request.POST.get('product_name', '').strip()
        username = request.POST.get('username', '').strip()
        price_str = request.POST.get('price', '0').strip()
        total_price_str = request.POST.get('total_price', '0').strip()
        quantity_str = request.POST.get('quantity', '1').strip()  # Default quantity to 1

        # Validate and convert data
        try:
            price = int(float(price_str)) if price_str else 0
            total_price = int(float(total_price_str)) if total_price_str else 0
            quantity = int(quantity_str) if quantity_str else 1
        except ValueError:
            messages.error(request, "Invalid input in the form.")
            return redirect('homepage')  # Redirect back to the homepage or the form page

        # Handle product image
        try:
            product = ProductDB.objects.get(name=product_name)
            product_image = product.image
        except ProductDB.DoesNotExist:
            product_image = None

        # Add or update the cart
        try:
            cart_item = CartDB.objects.get(ProductName=product_name, username=username)
            cart_item.Quantity += quantity  # Update quantity
            cart_item.TotalPrice = cart_item.Quantity * price  # Update total price
            cart_item.save()
        except CartDB.DoesNotExist:
            cart_item = CartDB(ProductName=product_name,username=username,Price=price,TotalPrice=total_price,Quantity=quantity,
                               Prod_Image=product_image)

        cart_item.save()
        messages.success(request, "Added to cart")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def delete_cart_item(request, cart_item_id):
    cart_item = CartDB.objects.get(id=cart_item_id)
    cart_item.delete()
    return redirect(cart)

def checkout(request):
    cart = CartDB.objects.filter(username=request.session['Username'])
    sub_total = 0
    shipping_amount = 0
    for i in cart:
        sub_total += i.TotalPrice

    if sub_total>1000:
        shipping_amount=100
    else:
        shipping_amount=200
    total_amount = sub_total+shipping_amount



    context = {'cartproducts': cart, 'subtotal': sub_total, 'shippingamount': shipping_amount, 'totalamount': total_amount}
    return render(request, "checkout.html", context)

def save_order(request):
    if request.method == "POST":
        name = request.POST.get('name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        place = request.POST.get('place')
        address = request.POST.get('address')
        mobile = request.POST.get('mobile')
        state = request.POST.get('state')
        pin = request.POST.get('pin')
        message = request.POST.get('message')
        total_price = request.POST.get('total_price')

        order = OrderDB(name=name,email=email,place=place,address=address,mobile=mobile,
                        state=state,pin=pin,message=message,total_price=total_price,username=username)
        order.save()
        return redirect('payment')
    else:
        return redirect('checkout')

def payment(request):
    cart = CartDB.objects.filter(username=request.session['Username'])
    sub_total = 0
    shipping_amount = 0
    for i in cart:
        sub_total += i.TotalPrice
    if sub_total > 1000:
        shipping_amount = 100
    else:
        shipping_amount = 200
    total_amount = sub_total + shipping_amount


    #Retreive the data from OrderDB with specified ID
    customer = OrderDB.objects.order_by('-id').first()
    payy = customer.total_price

    amount  = int(payy*100)

    payy_str = str(amount)


    if request.method == "POST":
        order_currency = 'INR'
        client = razorpay.Client(auth=('rzp_test_gI8v8djb3KFaLP', 't1fVvLOrj5kyW0C3MfFod1dZ'))
        payment = client.order.create({'amount': amount, 'currency': order_currency})
        print("Hello")


    context = {'cartproducts': cart, 'subtotal': sub_total, 'shippingamount': shipping_amount,
               'totalamount': total_amount, 'customer': customer, 'payy_str': payy_str}

    return render(request, "payment.html", context)


@csrf_exempt
def save_newsletter(request):
    if request.method == "POST":
        mail = request.POST.get('email')
        news = Newsletter(email=mail)
        news.save()
        messages.success(request, "You have successfully subscribed to the newsletter!")
    else:
        messages.warning(request, "Some error Occured")
    return redirect("homepage")



def about(request):
    return render(request,"about.html")

def blog(request):
    return render(request,"about.html")



