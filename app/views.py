from django.shortcuts import render, redirect, HttpResponse
from app.models import Category, Product, Contact, Order, Brand
from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.models import User
from app.forms import RegistrationForm
from django.contrib import messages

from django.contrib.auth.decorators import login_required
from cart.cart import Cart
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User

from django.views.decorators.cache import cache_control


# Create your views here.
def master(request):
    return render(request, 'master.html') 

#Homepage-----------------------------------------------------------------------------------------------
def index(request):
        category = Category.objects.all()
        product = Product.objects.all()
        brand = Brand.objects.all()
        
        brandID = request.GET.get('brand')
        categoryID = request.GET.get('category')
        if categoryID:
            product = Product.objects.filter(sub_category = categoryID).order_by('-id')
        elif brandID:
            product = Product.objects.filter(brand = brandID).order_by('-id')
        else:
            product = Product.objects.all()

        params = {'category' : category, 'product': product, 'brand': brand}
        return render(request, 'index.html', params)



#login, logout and register--------------------------------------------------------------------------
@cache_control(no_cache=True, must_revalidate=True)
def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(request.POST)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')  # Redirect to a success page or your desired URL
        else:
            # Authentication failed, display an error message or handle it as needed
            return render(request, 'login.html', {'error': 'Invalid credentials'})

    return render(request, 'login.html')

@cache_control(no_cache=True, must_revalidate=True)
def signup(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()  # Save the new user to the database
            return redirect('login')  # Redirect to the login page after successful registration
        else:
            errorss = form.errors
            messages.error(request, {'error': errorss})
    else:
        form = RegistrationForm()

    return render(request, 'signup.html')


def logout_user(request):
    logout(request)
    return redirect('login')


# Cart ---------------------------------------------------------------------------------------------------
@login_required(login_url="/users/login/")
def cart_add(request, id):
    product = Product.objects.get(pk=id)
    cart = Cart(request)
    cart.add(product)
    return redirect("index")


@login_required(login_url="/users/login/")
def item_remove(request, id):
    product = get_object_or_404(Product, pk=id)
    cart = Cart(request)
    cart.remove(product)
    return redirect("cart")


@login_required(login_url="/users/login/")
def item_increment(request, id):
    product = Product.objects.get(pk=id)
    cart = Cart(request)
    cart.add(product=product)
    return redirect("cart")


@login_required(login_url="/users/login/")
def item_decrement(request, id):
    product = Product.objects.get(pk=id)
    cart = Cart(request)
    cart.decrement(product=product)
    return redirect("cart")

@login_required(login_url="/users/login/")
def clear_cart(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart")


@login_required(login_url="/users/login/")
def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart.html', {'cart':cart})


#Contact US page----------------------------------------------------------------------------------
@login_required(login_url="/users/login/")
@cache_control(no_cache=True, must_revalidate=True)
def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        contact1 = Contact(name=name, email=email, subject=subject, message=message)
        contact1.save()
        messages.success(request, "Your Message has been Submitted")
    return render(request, 'contact.html')


#checkout in cart
@login_required(login_url="/users/login/")
@cache_control(no_cache=True, must_revalidate=True)
def checkout(request):
    if request.method == 'POST':
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        pincode = request.POST.get('pincode')
        cart = request.session.get('cart')
        uid = request.session.get('_auth_user_id')
        user = User.objects.get(pk=uid)

        for i in cart:
            a = int(cart[i]['quantity'])
            b = int(cart[i]['price'])
            total = a * b

            order = Order(
                user = user,
                phone = phone,
                address = address,
                pincode = pincode,
                product = cart[i]['name'],
                price = cart[i]['price'],
                quantity = cart[i]['quantity'],
                image = cart[i]['image'],
                total = total,
            )
            order.save()
            request.session['cart'] = {}       #so when we order and checkout the cart will get clear
        return redirect('/checkout/')
    else:                                                 #It should return a httpresponse or like this or it will throw error
        return redirect('index') 
    

#Your Order ----------------------------------------------------------------------------------------
@login_required(login_url="/users/login/")
@cache_control(no_cache=True, must_revalidate=True)
def your_order(request):
    uid = request.session.get('_auth_user_id')
    user = User.objects.get(pk=uid)

    order = Order.objects.filter(user = user)                   #here we have use filter so that it shows oproduct of the users only which he has ordered, by using filter(user = user) first user is our model user and second is the variable
    params = {
        'order' : order,
    }
    return render(request, 'your_order.html', params)


#product Detail
@cache_control(no_cache=True, must_revalidate=True)
def prod_detail(request,id):
    category = Category.objects.all()
    product = Product.objects.all()
    brand = Brand.objects.all()
    
    brandID = request.GET.get('brand')                                                                     #from here we have copied from INDEX VIEW so to fetch and should redirect to subcategory and category products
    categoryID = request.GET.get('category')
    if categoryID:
        product = Product.objects.filter(sub_category = categoryID).order_by('-id')
    elif brandID:
        product = Product.objects.filter(brand = brandID).order_by('-id')
    else:
        product = Product.objects.all()                                                                     # Till here copied FROM INDEX VIEW CODE.

    product = Product.objects.filter(pk=id).first()
    params = {'product': product, 'category':category, 'brand':brand}
    return render(request, 'prod_detail.html', params)


#product detail
@cache_control(no_cache=True, must_revalidate=True) 
def prod_search(request):
    search = request.GET.get('search')
    product = Product.objects.filter(name__icontains = search)
    params = {'product': product, 'search': search}
    return render(request, 'search.html', params)