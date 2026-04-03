from django.shortcuts import render,redirect
from django.contrib.auth.models import *
from django.contrib import auth,messages
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
import random
from .models import *
 
# Create your views here.

def login(request):
    if request.method=='POST':
        email = request.POST['email']
        password=request.POST['password']
        query1=Login.objects.filter(email=email,password=password).exists()
        if query1:
            query2=Login.objects.get(email=email,password=password)
            request.session["lid"]=query2.pk
            lid=request.session.get('lid')
            if query2.user_type=='admin':
                return redirect('adminhome')
            elif query2.user_type=='user':
                u=User.objects.get(LOGIN=lid)
                request.session["user_id"]=u.pk
                return redirect('index')
            elif query2.user_type=='staff':
                s=Staff.objects.get(LOGIN=lid)
                request.session["staff_id"]=s.pk
                return redirect('staffhome')
        messages.error(request, "Invalid email or password")
        return redirect('login')
    return render(request,'login.html')



def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = Login.objects.get(email=email)
            
            otp = str(random.randint(100000, 999999))
            request.session['forgot_email'] = email
            request.session['forgot_otp'] = otp

            send_mail(
                'OTP for Password Reset',
                f'Your OTP for password reset is: {otp}',
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False
            )

            messages.success(request, "OTP sent to your email.")
            return redirect('verify_otp')

        except Login.DoesNotExist:
            messages.error(request, "Email not registered.")
    
    return render(request, 'forgot_password.html')


def verify_otp(request):
    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        session_otp = request.session.get('forgot_otp')
        
        if entered_otp == session_otp:
            messages.success(request, "OTP verified. Set your new password.")
            return redirect('reset_password')
        else:
            messages.error(request, "Invalid OTP.")
    
    return render(request, 'verify_otp.html')


def reset_password(request):
    email = request.session.get('forgot_email')
    if not email:
        messages.error(request, "Session expired. Try again.")
        return redirect('forgot_password')

    if request.method == 'POST':
        new_password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if new_password != confirm_password:
            messages.error(request, "Passwords do not match.")
        else:
            try:
                user = Login.objects.get(email=email)
                user.password = new_password 
                user.save()
                
                request.session.pop('forgot_email')
                request.session.pop('forgot_otp')
                
                messages.success(request, "Password reset successfully.")
                return redirect('login')
            except Login.DoesNotExist:
                messages.error(request, "User not found.")
    return render(request, 'reset_password.html')


def delete_product_admin(request, id):
    Productsnacks.objects.filter(id=id).delete()
    Productbeverages.objects.filter(id=id).delete()
    Productvegitable.objects.filter(id=id).delete()
    Productrice.objects.filter(id=id).delete()
    Productfruits.objects.filter(id=id).delete()
    Productmilk.objects.filter(id=id).delete()
    Productegg.objects.filter(id=id).delete()
    Productfish.objects.filter(id=id).delete()
    return redirect('adminhome')


def delete_product_staff(request, id):
    Productsnacks.objects.filter(id=id).delete()
    Productbeverages.objects.filter(id=id).delete()
    Productvegitable.objects.filter(id=id).delete()
    Productrice.objects.filter(id=id).delete()
    Productfruits.objects.filter(id=id).delete()
    Productmilk.objects.filter(id=id).delete()
    Productegg.objects.filter(id=id).delete()
    Productfish.objects.filter(id=id).delete()
    return redirect('staffhome')





def about(request):
    return render(request,'about.html')

def contact(request):
    return render(request,'contact.html')


def service(request):
    return render(request,'service.html')

def logout(request):
    request.session.flush()
    return redirect('login')

def user_register(request):
    if request.method=='POST':
        username=request.POST['username']
        firstname=request.POST['firstname']
        lastname=request.POST['lastname']
        email=request.POST['email']
        phone=request.POST['phone']
        password=request.POST['password']

        q1=Login.objects.create(email=email,password=password,user_type='user')
        q1.save()

        q2=User.objects.create(username=username,firstname=firstname,lastname=lastname,phone=phone,LOGIN_id=q1.pk)
        
        q2.save()
        return redirect('login')
    return render(request,'user_register.html')


def profile_view_edit(request,id):
    old_data=User.objects.get(id=id)
    if request.method=='POST':
        username=request.POST['username']
        firstname=request.POST['firstname']
        lastname=request.POST['lastname']
        phone=request.POST['phone']
        old_data.username=username    
        old_data.firstname=firstname    
        old_data.lastname=lastname  
        old_data.phone=phone   
        old_data.save() 
        return redirect('profile_view')
    return render(request,'profile_view_edit.html',{'result':old_data})


def staff_register(request):
    if request.method=='POST':
        username=request.POST['username']
        firstname=request.POST['firstname']
        lastname=request.POST['lastname']
        dob=request.POST['dob']
        email=request.POST['email']
        phone=request.POST['phone']
        password=request.POST['password']

        q1=Login.objects.create(email=email,password=password,user_type='staff')
        q1.save()

        q2=Staff.objects.create(username=username,firstname=firstname,lastname=lastname,dob=dob,phone=phone,LOGIN_id=q1.pk)
        q2.save()
        return redirect('staff_admin_view')
    return render(request,'staff_register.html')



def adminhome(request):
    Ps = Productsnacks.objects.all()
    Pv = Productvegitable.objects.all()
    Pb = Productbeverages.objects.all()
    Pf = Productfruits.objects.all()
    Pe=Productegg.objects.all()
    Pfi=Productfish.objects.all()
    Pr=Productrice.objects.all()
    Pm=Productmilk.objects.all()
    return render(request,'adminhome.html', {'result': Ps, 'vegi': Pv, 'bev': Pb, 'fru': Pf,'egg':Pe,'pfi':Pfi,'pr':Pr,'pm':Pm})


def staff_admin_view(request):
    staff=Staff.objects.all()
    return render(request,'staff_admin_view.html',{'result':staff})

def users_view_admin(request):
    user=User.objects.all()
    return render(request,'users_view_admin.html',{'result':user})

def complaint_view(request):
    c=Complaint.objects.all()
    return render(request,'complaint_view.html',{'result':c})

def response(request):
    user_id=request.session["user_id"]
    if request.method=='POST':
        responder=request.POST['responder']
        response=request.POST['response']
        status=request.POST['status']
        sendresponde=Response.objects.create(responder=responder,response=response,status=status,USER_id=user_id)
        sendresponde.save()
        return redirect('adminhome')
    return render(request,'response.html')

def responde_view_user(request):
    user_id=request.session["user_id"]
    r=Response.objects.filter(USER_id=user_id)
    return render(request,'responde_view_user.html',{'result':r})


# def product_snack(request):
#     if request.method=='POST':
#         image = request.FILES['image']
#         name=request.POST['name']
#         price=request.POST['price']
#         p=Productsnacks.objects.create(image=image,name=name,price=price)
#         p.save()
#         return redirect('index')
#     return render(request,'product_snack.html')

def product_snack(request):
    if request.method=='POST':
        image = request.FILES.get('image')
        name = request.POST.get('name')
        price = request.POST.get('price')
        stock = request.POST.get('stock', 0)
        p=Productsnacks.objects.create(image=image,name=name,price=price,stock=stock)
        p.save() 
    return render(request, 'product_snack.html')

def product_snack_edit(request,id):
    old_data=Productsnacks.objects.get(id=id)
    if request.method=='POST':
        image = request.FILES.get('image')
        name = request.POST.get('name')
        price = request.POST.get('price')
        stock = request.POST.get('stock', 0)

        if image:
            old_data.image=image
        old_data.name=name
        old_data.price=price
        old_data.stock=stock
        old_data.save()
        return redirect('staffhome')
    return render(request,'product_snack_edit.html',{'result':old_data})


def staffhome(request):
    edit1=Productsnacks.objects.all()
    edit2=Productvegitable.objects.all()
    edit3=Productbeverages.objects.all()
    edit4=Productfruits.objects.all()
    edit5=Productegg.objects.all()
    edit6=Productfish.objects.all()
    edit7=Productrice.objects.all()
    edit8=Productmilk.objects.all()
    return render(request,'staffhome.html',{'result_1':edit1, 'result_2':edit2, 'result_3':edit3, 'result_4':edit4,'result_5':edit5,'result_6':edit6,'result_7':edit7,'result_8':edit8})


def staff_view_profile(request):
    staff_id=request.session["staff_id"]
    staff=Staff.objects.filter(id=staff_id)
    return render(request,'staff_view_profile.html',{'result':staff})


def index(request):
    Ps=Productsnacks.objects.all()
    Pv=Productvegitable.objects.all()
    Pb=Productbeverages.objects.all()
    Pf=Productfruits.objects.all()
    return render(request,'index.html',{'result':Ps,'vegi':Pv,'bev':Pb,'fru':Pf})


def product_vegitable(request):
    if request.method=='POST':
        image = request.FILES.get('image')
        name = request.POST.get('name')
        price = request.POST.get('price')
        stock = request.POST.get('stock', 0)
        kg = request.POST.get('kg') 
        p=Productvegitable.objects.create(image=image,name=name,price=price,stock=stock,kg=kg)
        p.save()
    return render(request,'product_vegitable.html')

def product_vegitable_edit(request,id):
    old_data=Productvegitable.objects.get(id=id)
    if request.method=='POST':
        image = request.FILES.get('image')
        name = request.POST.get('name')
        price = request.POST.get('price')
        stock = request.POST.get('stock', 0)
        kg = request.POST.get('kg')

        if image:
            old_data.image=image
        old_data.name=name 
        old_data.price=price 
        old_data.stock=stock 
        old_data.kg=kg
        old_data.save() 
        return redirect('staffhome')
    return render(request,'product_vegitable_edit.html',{'result':old_data})


def vegitable_pageview(request):
    s=Productvegitable.objects.all()
    return render(request,'vegitable_pageview.html',{'result':s})


def snack_pageview(request):
    s=Productsnacks.objects.all()
    return render(request,'snack_pageview.html',{'result':s})


def product_beverages(request):
    if request.method=='POST':
        image = request.FILES.get('image')
        name = request.POST.get('name')
        price = request.POST.get('price')
        stock = request.POST.get('stock', 0)
        liter = request.POST.get('liter')
        p=Productbeverages.objects.create(image=image,name=name,price=price,stock=stock,liter=liter)
        p.save()
    return render(request,'product_beverages.html')


def product_beverages_edit(request,id):
    old_data=Productbeverages.objects.get(id=id)
    if request.method=='POST':
        image = request.FILES.get('image')
        name = request.POST.get('name')
        price = request.POST.get('price')
        stock = request.POST.get('stock', 0)
        liter = request.POST.get('liter')

        if image:
            old_data.image=image
        old_data.name=name
        old_data.price=price
        old_data.stock=stock
        old_data.liter=liter
        old_data.save()
        return redirect('staffhome')
    return render(request,'product_beverages_edit.html')



def beverage_pageview(request):
    s=Productbeverages.objects.all()
    return render(request,'beverage_pageview.html',{'result':s})


def product_fruits(request):
    if request.method=='POST':
        image = request.FILES.get('image')
        name = request.POST.get('name')
        price = request.POST.get('price')
        stock = request.POST.get('stock', 0)
        kg = request.POST.get('kg') 
        p=Productfruits.objects.create(image=image,name=name,price=price,stock=stock,kg=kg)
        p.save()
    return render(request,'product_fruits.html')

def product_fruits_edit(request,id):
    old_data=Productfruits.objects.get(id=id)
    if request.method=='POST':
        image = request.FILES.get('image')
        name = request.POST.get('name')
        price = request.POST.get('price')
        stock = request.POST.get('stock', 0)
        kg = request.POST.get('kg')

        if image:
            old_data.image=image
        old_data.name=name
        old_data.price=price
        old_data.stock=stock
        old_data.kg=kg
        old_data.save()
        return redirect('staffhome')
    return render(request,'product_fruits_edit.html',{'result':old_data})

def fruits_pageview(request):
    s=Productfruits.objects.all()
    return render(request,'fruits_pageview.html',{'result':s})


def product_egg(request):
    if request.method == 'POST':
        image = request.FILES.get('image')
        stock = request.POST.get('stock',0)
        name = request.POST.get('name')
        price_per_egg = request.POST.get('price_per_egg')
        e=Productegg.objects.create(image=image,stock=stock,name=name,price_per_egg=price_per_egg)
        e.save()
    return render(request, 'product_egg.html')


def product_egg_edit(request,id):
    old_data=Productegg.objects.get(id=id)
    if request.method=='POST':
        image = request.FILES.get('image')
        name = request.POST.get('name')
        price_per_egg = request.POST.get('price_per_egg')
        stock = request.POST.get('stock', 0)

        if image:
            old_data.image=image
        old_data.name=name
        old_data.price_per_egg=price_per_egg
        old_data.stock=stock
        old_data.save()
        return redirect('')
    return render(request,'product_egg_edit.html',{'result':old_data})    


def egg_pageview(request):
    s=Productegg.objects.all()
    return render(request,'egg_pageview.html',{'result':s})


def product_fish(request):
    if request.method == 'POST':
        image = request.FILES.get('image')
        stock = request.POST.get('stock', 0)
        name = request.POST.get('name')
        kg = request.POST.get('kg')
        price = request.POST.get('price')

        f=Productfish.objects.create( image=image,stock=stock, name=name,kg=kg, price=price)
        f.save()
    return render(request, 'product_fish.html')


def product_fish_edit(request,id):
    old_data=Productfish.objects.get(id=id)
    if request.method=='POST':
        image = request.FILES.get('image')
        name = request.POST.get('name')
        price = request.POST.get('price')
        stock = request.POST.get('stock', 0)
        kg=request.POST.get('kg')

        if image:
            old_data.image=image
        old_data.name=name
        old_data.price=price
        old_data.stock=stock
        old_data.kg=kg
        old_data.save()
        return redirect('staffhome')
    return render(request,'product_fish_edit.html',{'result':old_data}) 

def fish_pageview(request):
    s=Productfish.objects.all()
    return render(request,'fish_pageview.html',{'result':s})


def product_rice(request):
    if request.method == 'POST':
        image = request.FILES.get('image')
        name = request.POST.get('name')
        stock = request.POST.get('stock')
        kg = request.POST.get('kg')
        price = request.POST.get('price')
        r=Productrice.objects.create(image=image,name=name,stock=stock,kg=kg,price=price)
        r.save()  
    return render(request, 'product_rice.html')

def rice_pageview(request):
    r=Productrice.objects.all()
    return render(request,'rice_pageview.html',{'result':r})


def product_rice_edit(request,id):
    old_data=Productrice.objects.get(id=id)
    if request.method=='POST':
        image = request.FILES.get('image')
        name = request.POST.get('name')
        price = request.POST.get('price')
        stock = request.POST.get('stock', 0)
        kg=request.POST.get('kg')

        if image:
            old_data.image=image
        old_data.name=name
        old_data.price=price
        old_data.stock=stock
        old_data.kg=kg
        old_data.save()
        return redirect('staffhome')
    return render(request,'product_rice_edit.html',{'result':old_data}) 

def product_milk(request):
    if request.method == 'POST':
        image = request.FILES.get('image')
        name = request.POST.get('name')
        stock = request.POST.get('stock')
        litre = request.POST.get('litre', "litre")
        price = request.POST.get('price')
        r=Productmilk.objects.create(image=image,name=name,stock=stock,litre=litre,price=price)
        r.save()  
    return render(request, 'product_milk.html')


def milk_pageview(request):
    m=Productmilk.objects.all()
    return render(request,'milk_pageview.html',{'result':m})


def product_milk_edit(request,id):
    old_data=Productmilk.objects.get(id=id)
    if request.method=='POST':
        image = request.FILES.get('image')
        name = request.POST.get('name')
        price = request.POST.get('price')
        stock = request.POST.get('stock', 0)
        litre=request.POST.get('litre')

        if image:
            old_data.image=image
        old_data.name=name
        old_data.price=price
        old_data.stock=stock
        old_data.litre=litre
        old_data.save()
        return redirect('staffhome')
    return render(request,'product_milk_edit.html',{'result':old_data}) 


def shop(request):
    Ps = Productsnacks.objects.all()
    Pv = Productvegitable.objects.all()
    Pb = Productbeverages.objects.all()
    Pf = Productfruits.objects.all()
    pe=Productegg.objects.all()
    pfi=Productfish.objects.all()
    pr=Productrice.objects.all()
    pm=Productmilk.objects.all()
    return render(request, 'shop.html', {'result': Ps, 'vegi': Pv, 'bev': Pb, 'fru': Pf,'egg':pe,'fish':pfi,'pr':pr,'pm':pm})



# def snack_cart(request, id):
#     snacks = Productsnacks.objects.filter(id=id)
#     return render(request, 'snack_cart.html', {'result': snacks})

def snack_cart(request, id):
    user_id = request.session.get("user_id")
    if not user_id:
        return redirect("login")
    user = User.objects.filter(id=user_id).first()
    if not user:
        request.session.flush()
        return redirect("login")
    snack = Productsnacks.objects.filter(id=id).first()
    if not snack:
        return redirect("shop")
    if request.method == "POST":
        quantity = int(request.POST.get("quantity", 1))
        existing_item = Cart.objects.filter(USER=user, SNACKS=snack).first()
        current_qty = existing_item.quantity if existing_item else 0
        if current_qty + quantity > snack.stock:
            messages.error(
                request,
                f"Only {snack.stock - current_qty} items available in stock"
            )
            return redirect("snack_cart", id=id)
        if existing_item:
            existing_item.quantity += quantity
            existing_item.save()
        else:
            Cart.objects.create(
                USER=user,
                SNACKS=snack,
                quantity=quantity
            )
        return redirect("view_cart")
    snack_review = Review.objects.filter(ORDER_ITEM__SNACKS_id=id)
    return render(request,"snack_cart.html",{"result": snack,"snack_review": snack_review})

# def vegitable_cart(request,id):
#     vegitable=Productvegitable.objects.filter(id=id)
#     return render(request,'vegitable_cart.html',{'result':vegitable})

def vegitable_cart(request, id):
    user_id = request.session.get("user_id")
    if not user_id:
        return redirect("login")
    user = User.objects.filter(id=user_id).first()
    if not user:
        request.session.flush()
        return redirect("login")
    veg = Productvegitable.objects.filter(id=id).first()
    if not veg:
        return redirect("shop")
    if request.method == "POST":
        quantity = int(request.POST.get("quantity", 1))
        existing_item = Cart.objects.filter(USER=user, VEGITABLES=veg).first()
        current_qty = existing_item.quantity if existing_item else 0
        if current_qty + quantity > veg.stock:
            messages.error(
                request,
                f"Only {veg.stock - current_qty} items available in stock")
            return redirect("vegitable_cart", id=id)
        if existing_item:
            existing_item.quantity += quantity
            existing_item.save()
        else:
            Cart.objects.create(USER=user,VEGITABLES=veg,quantity=quantity)
        return redirect("view_cart")
    vegitable_review = Review.objects.filter(ORDER_ITEM__VEGITABLES_id=id)
    return render(request,"vegitable_cart.html",{"result": [veg],"vegitable_review": vegitable_review})

# def beverges_cart(request,id):
#     fruit=Productbeverages.objects.filter(id=id)
#     return render(request,'beverges_cart.html',{'result':fruit})

def beverges_cart(request, id):
    user_id = request.session.get("user_id")
    if not user_id:
        return redirect("login")
    user = User.objects.get(id=user_id)
    beverage = Productbeverages.objects.filter(id=id).first()
    if not beverage:
        return redirect("shop")
    if request.method == "POST":
        quantity = int(request.POST.get("quantity", 1))
        existing_item = Cart.objects.filter(USER=user, BEVERAGES=beverage).first()
        current_qty = existing_item.quantity if existing_item else 0
        if current_qty + quantity > beverage.stock:
            messages.error(
                request,
                f"Only {beverage.stock - current_qty} items available in stock"
            )
            return redirect('beverges_cart', id=id)
        if existing_item:
            existing_item.quantity += quantity
            existing_item.save()
        else:
            Cart.objects.create(
                USER=user,
                BEVERAGES=beverage,
                quantity=quantity
            )
        return redirect("view_cart")
    beverage_review = Review.objects.filter(ORDER_ITEM__BEVERAGES_id=id)
    return render(request,"beverges_cart.html",{"result": [beverage],"beverage_review": beverage_review})

# def fruit_cart(request,id):
#     fruit=Productfruits.objects.filter(id=id)
#     return render(request,'fruit_cart.html',{'result':fruit})

def fruit_cart(request, id):
    user_id = request.session.get("user_id")
    if not user_id:
        return redirect("login")
    user = User.objects.filter(id=user_id).first()
    if not user:
        request.session.flush()
        return redirect("login")
    fruit = Productfruits.objects.filter(id=id).first()
    if not fruit:
        return redirect("shop")
    if request.method == "POST":
        quantity = int(request.POST.get("quantity", 1))
        existing_item = Cart.objects.filter(USER=user, FRUITS=fruit).first()
        current_qty = existing_item.quantity if existing_item else 0
        if current_qty + quantity > fruit.stock:
            messages.error(
                request,
                f"Only {fruit.stock - current_qty} items available in stock")
            return redirect("fruit_cart", id=id)
        if existing_item:
            existing_item.quantity += quantity
            existing_item.save()
        else:
            Cart.objects.create(
                USER=user,
                FRUITS=fruit,
                quantity=quantity
            )
        return redirect("view_cart")
    fruit_review = Review.objects.filter(ORDER_ITEM__FRUITS_id=id)
    return render(request,"fruit_cart.html",{"result": [fruit],"fruits_review": fruit_review})


def egg_cart(request, id):
    user_id = request.session.get("user_id")
    if not user_id:
        return redirect("login")
    user = User.objects.filter(id=user_id).first()
    if not user:
        request.session.flush()
        return redirect("login")
    egg = Productegg.objects.filter(id=id).first()
    if not egg:
        return redirect("shop")
    if request.method == "POST":
        quantity = int(request.POST.get("quantity", 1))
        existing_item = Cart.objects.filter(USER=user, EGGS=egg).first()
        current_qty = existing_item.quantity if existing_item else 0
        if current_qty + quantity > egg.stock:
            messages.error(
                request,
                f"Only {egg.stock - current_qty} items available in stock"
            )
            return redirect("egg_cart", id=id)

        if existing_item:
            existing_item.quantity += quantity
            existing_item.save()
        else:
            Cart.objects.create(
                USER=user,
                EGGS=egg,
                quantity=quantity
            )
        return redirect("view_cart")
    egg_review = Review.objects.filter(ORDER_ITEM__EGGS_id=id)
    return render(request,"egg_cart.html",{"result": [egg],"egg_review": egg_review})


def fish_cart(request, id):
    user_id = request.session.get("user_id")
    if not user_id:
        return redirect("login")
    user = User.objects.filter(id=user_id).first()
    if not user:
        request.session.flush()
        return redirect("login")
    fish = Productfish.objects.filter(id=id).first()
    if not fish:
        return redirect("shop")
    if request.method == "POST":
        quantity = int(request.POST.get("quantity", 1))
        existing_item = Cart.objects.filter(USER=user, FISH=fish).first()
        current_qty = existing_item.quantity if existing_item else 0
        if current_qty + quantity > fish.stock:
            messages.error(
                request,
                f"Only {fish.stock - current_qty} items available in stock")
            return redirect("fish_cart", id=id)
        if existing_item:
            existing_item.quantity += quantity
            existing_item.save()
        else:
            Cart.objects.create(
                USER=user,
                FISH=fish,
                quantity=quantity
            )
        return redirect("view_cart")
    fish_review = Review.objects.filter(ORDER_ITEM__FISH_id=id)
    return render(request,"fish_cart.html",{"result": [fish],"fish_review": fish_review})
   

def rice_cart(request, id):
    user_id = request.session.get("user_id")
    if not user_id:
        return redirect("login")
    user = User.objects.filter(id=user_id).first()
    if not user:
        request.session.flush()
        return redirect("login")
    rice = Productrice.objects.filter(id=id).first()
    if not rice:
        return redirect("shop")
    if request.method == "POST":
        quantity = int(request.POST.get("quantity", 1))
        existing_item = Cart.objects.filter(USER=user, RICE=rice).first()
        current_qty = existing_item.quantity if existing_item else 0
        if current_qty + quantity > rice.stock:
            messages.error(
                request,
                f"Only {rice.stock - current_qty} items available in stock"
            )
            return redirect("rice_cart", id=id)
        if existing_item:
            existing_item.quantity += quantity
            existing_item.save()
        else:
            Cart.objects.create(
                USER=user,
                RICE=rice,
                quantity=quantity
            )
        return redirect("view_cart")
    rice_review = Review.objects.filter(ORDER_ITEM__RICE_id=id)
    return render(request,"rice_cart.html",{"result": rice,"rice_review": rice_review})


def milk_cart(request, id):
    user_id = request.session.get("user_id")
    if not user_id:
        return redirect("login")
    user = User.objects.filter(id=user_id).first()
    if not user:
        request.session.flush()
        return redirect("login")
    milk = Productmilk.objects.filter(id=id).first()
    if not milk:
        return redirect("shop")
    if request.method == "POST":
        quantity = int(request.POST.get("quantity", 1))
        existing_item = Cart.objects.filter(USER=user, MILK=milk).first()
        current_qty = existing_item.quantity if existing_item else 0
        if current_qty + quantity > milk.stock:
            messages.error(
                request,
                f"Only {milk.stock - current_qty} items available in stock"
            )
            return redirect("milk_cart", id=id)
        if existing_item:
            existing_item.quantity += quantity
            existing_item.save()
        else:
            Cart.objects.create(
                USER=user,
                MILK=milk,
                quantity=quantity
            )
        return redirect("view_cart")
    milk_review = Review.objects.filter(ORDER_ITEM__MILK_id=id)
    return render(request,"milk_cart.html",{"result": milk,"milk_review": milk_review})

def view_cart(request):
    user_id = request.session.get("user_id")
    cart_items = Cart.objects.filter(USER_id=user_id)
    total_price = 0

    for item in cart_items:
        product = next(
            (getattr(item, field) for field in ["FRUITS", "VEGITABLES", "SNACKS", 
                                                "BEVERAGES", "EGGS", "FISH", "RICE", "MILK"] 
             if getattr(item, field) is not None), 
            None
        )

        if product:
            price = product.price
        else:
            price = 0

        item.total_price = price * item.quantity
        total_price += item.total_price

    context = {
        "cart_items": cart_items,
        "total_price": total_price
    }
    return render(request, "view_cart.html", context)


def remove_cart(request, id):
    cart_item = Cart.objects.get(id=id)
    cart_item.delete()
    return redirect('view_cart')

def increase_qty(request, item_id):
    item = Cart.objects.get(id=item_id)
    product = None
    if item.EGGS:
        product = item.EGGS
    elif item.FISH:
        product = item.FISH
    elif item.SNACKS:
        product = item.SNACKS
    elif item.VEGITABLES:
        product = item.VEGITABLES
    elif item.FRUITS:
        product = item.FRUITS
    elif item.BEVERAGES:
        product = item.BEVERAGES
    elif item.RICE:
        product = item.RICE
    elif item.MILK:
        product = item.MILK
    if product and item.quantity < product.stock:
        item.quantity += 1
        item.save()
    else:
        messages.error(request, "Out Of Stock")
    return redirect('view_cart')


def decrease_qty(request, item_id):
    item = Cart.objects.get(id=item_id)

    if item.SNACKS:
        product = item.SNACKS
    elif item.FRUITS:
        product = item.FRUITS
    elif item.VEGITABLES:
        product = item.VEGITABLES
    elif item.BEVERAGES:
        product = item.BEVERAGES
    elif item.EGGS:
        product = item.EGGS
    elif item.FISH:
        product = item.FISH  
    elif item.RICE:
        product = item.RICE
    elif item.MILK:
        product = item.MILK  
    else:
        messages.error(request, "No product found!")
        return redirect('view_cart')

    if item.quantity > 1:
        item.quantity -= 1
        item.save()
    else:
        messages.error(request, "Minimum quantity is 1!")
    return redirect('view_cart')


def complaint(request):
    user_id=request.session["user_id"]
    if request.method=='POST':
        image=request.FILES.get('image')
        email=request.POST['email']
        phone=request.POST['phone']
        category=request.POST['category']
        subject=request.POST['subject']
        c=Complaint.objects.create(image=image,email=email,phone=phone,category=category,subject=subject,USER_id=user_id)
        c.save()
        return redirect('profile_view')
    return render(request,'complaint.html')

def profile_view(request):
    user_id = request.session.get("user_id")
    if not user_id:
        return redirect("login") 
    user = User.objects.filter(id=user_id).first()
    if not user:
        return redirect("login")
    return render(request, "profile_view.html", {"user": user})



def add_address(request):
    user_id = request.session.get("user_id")
    if not user_id:
        return redirect("login")

    if request.method == "POST":
        house_name = request.POST.get("house_name")
        fullname = request.POST.get("fullname")
        city = request.POST.get("city")
        state = request.POST.get("state")
        district = request.POST.get("district")
        landmark = request.POST.get("landmark")
        pincode = request.POST.get("pincode")
        phone = request.POST.get("phone")

        if str(pincode) != settings.DELIVERY_PINCODE:
            messages.error(
                request,
                "Sorry! FreshMart currently delivers only to pincode 688005."
            )
            return redirect("add_address")

        Address.objects.create(
            USER_id=user_id,
            housename =house_name,
            fullname=fullname,
            city=city,
            state=state,
            district=district,
            pincode=pincode,
            landmark=landmark,
            phone=phone
        )

        messages.success(request, "Address added successfully!")
        return redirect("checkout")

    return render(request, "add_address.html")




def checkout(request):
    user_id = request.session.get("user_id")
    if not user_id:
        return redirect("login")
    address = Address.objects.filter(USER_id=user_id)
    return render(request, "checkout.html", {"address": address})




def place_order(request):
    user_id = request.session.get("user_id")
    if not user_id:
        return redirect("login")

    cart_items = Cart.objects.filter(USER_id=user_id)
    if not cart_items.exists():
        return redirect("view_cart")

    address_id = request.POST.get("address_id")
    payment_method = request.POST.get("payment_method")
    address = Address.objects.get(id=address_id)

    order = Order.objects.create(
        USER_id=user_id,
        ADDRESS=address,
        payment_method=payment_method,
        total_price=0
    )

    total_amount = 0

    for item in cart_items:
        product = item.SNACKS or item.FRUITS or item.VEGITABLES or \
                  item.BEVERAGES or item.EGGS or item.FISH or \
                  item.RICE or item.MILK

        if product.stock < item.quantity:
            messages.error(request, f"Not enough stock for {product.name}")
            order.delete()
            return redirect("view_cart")

        product.stock -= item.quantity
        product.save()

        price = product.price
        qty = item.quantity
        total_amount += price * qty

        OrderItem.objects.create(
            ORDER=order,
            SNACKS=item.SNACKS,
            FRUITS=item.FRUITS,
            VEGITABLES=item.VEGITABLES,
            BEVERAGES=item.BEVERAGES,
            EGGS=item.EGGS,
            FISH=item.FISH,
            RICE=item.RICE,
            MILK=item.MILK,
            quantity=qty,
            price=price
        )

    order.total_price = total_amount
    order.save()

    # 🔥 Get admin & staff emails
    admin_staff_logins = Login.objects.filter(
        user_type__in=['admin', 'staff']
    ).values_list('email', flat=True)

    # 📧 Send Email
    send_mail(
        subject=f"New Order #{order.id}",
        message=f"""
New Order Placed!

Order ID: {order.id}
Total Amount: ₹{total_amount}
Payment Method: {payment_method}
""",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=list(admin_staff_logins),
        fail_silently=False,
    )
    cart_items.delete()
    return redirect("order_success")



def order_success(request):
    return render(request, 'order_success.html')



def orders(request):
    user_id = request.session.get('user_id')
    current_orders = Order.objects.filter(USER_id=user_id).exclude(STATUS="Delivered").order_by('-order_date')
    history_orders = Order.objects.filter(USER_id=user_id,STATUS="Delivered").order_by('-order_date')
    context = {'current_orders': current_orders,'history_orders': history_orders}
    return render(request, 'orders.html', context)


def return_item(request, item_id):
    item_qs = OrderItem.objects.filter(id=item_id)

    if not item_qs.exists():
        return redirect('orders')

    item = item_qs.first()
    
    if item.ORDER.STATUS != "Delivered":
        return redirect('orders')

    already_returned = ReturnRequest.objects.filter(ORDER_ITEM=item).exists()
    if already_returned:
        return redirect('orders')


    if request.method == "POST":
        reason = request.POST.get("reason")
        ReturnRequest.objects.create(ORDER_ITEM=item, reason=reason)
        subject = "New Return Request - Freshmart"

        message = f"""
        A new return request has been submitted.

        Order ID: {item.ORDER.id}
        User: {item.ORDER.USER.username}
        Product: {item}
        Reason: {reason}
        """

        admin_staff_logins = Login.objects.filter(
        user_type__in=['admin', 'staff']).values_list('email', flat=True)

        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            recipient_list=list(admin_staff_logins),
            fail_silently=False,
        )
        return redirect('orders')
    return render(request, "return_item.html", {"item": item})


def track_return(request, item_id):
    item = OrderItem.objects.filter(id=item_id).first()
    if not item:
        return redirect('orders')
    return_request = ReturnRequest.objects.filter(ORDER_ITEM=item).first()
    return render(request,"track_return.html", {"item": item,"return_request": return_request})




def update_order_status(request, order_id):
    if not request.user.is_staff:
        return redirect('home')
    order = Order.objects.filter(id=order_id).first()
    if not order:
        return redirect("staff_update_order") 
    new_status = request.POST.get("status")
    if new_status:
        order.STATUS = new_status
        order.save()
    return redirect("staff_update_order")


def cancel_order(request, order_id):
    user_id=request.session["user_id"]
    order_qs = Order.objects.filter(id=order_id, USER=user_id)
    if order_qs.exists():
        order = order_qs.first()
    if order.STATUS not in ['Delivered', 'Cancelled']:
        order.STATUS = 'Cancelled'
        order.save()
    return redirect('orders')


def track_order(request, order_id):
    order = Order.objects.get(id=order_id)
    steps = ["Confirmed", "Prepared", "Out for Delivery", "Delivered"]
    if order.STATUS == "Confirmed":
        status_number = 0
    elif order.STATUS == "Prepared":
        status_number = 1
    elif order.STATUS == "Out for Delivery":
        status_number = 2
    elif order.STATUS == "Delivered":
        status_number = 3
    else:
        status_number = -1  
    return render(request, "track_order.html", {"order": order,"steps": steps,"status_number": status_number})



def staff_update_order(request):
    if request.method == "POST":
        order_id = request.POST.get("order_id")
        new_status = request.POST.get("STATUS")
        order = Order.objects.filter(id=order_id).first()
        if order:
            order.STATUS = new_status
            order.save()
            if order.USER and order.USER.LOGIN.email:
                send_mail(
                    subject="Your Order Status Updated",
                    message=f"Hello {order.USER.username},\n\n"
                            f"Your order #{order.id} status has been updated to: {new_status}.\n\n"
                            f"Thank you for shopping with us!",
                    from_email="yourgmail@gmail.com",
                    recipient_list=[order.USER.LOGIN.email],   
                    fail_silently=False,
                )
        return redirect('staff_update_order')
    current_orders = Order.objects.exclude(STATUS__in=["Delivered", "Cancelled"]).order_by('-order_date')
    history_orders = Order.objects.filter(STATUS__in=["Delivered", "Cancelled"]).order_by('-order_date')
    return render(request, "staff_update_order.html", {"current_orders": current_orders,"history_orders": history_orders,})



def staff_update_return_order(request):
    if request.method == "POST":
        return_id = request.POST.get("return_id")
        new_status = request.POST.get("RETURN_STATUS")

        return_request = ReturnRequest.objects.filter(id=return_id).first()

        if return_request:
            return_request.status = new_status
            return_request.save()

            order = return_request.ORDER_ITEM.ORDER
            if order.USER and order.USER.LOGIN.email:
                send_mail(
                    subject="Your Return Status Updated",
                    message=f"Hello {order.USER.username},\n\n"
                            f"Your return request for Order #{order.id} "
                            f"has been updated to: {new_status}.\n\n"
                            f"Thank you for shopping with us!",
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[order.USER.LOGIN.email],
                    fail_silently=False,)

        return redirect('staff_update_return_order')
    return_requests = ReturnRequest.objects.all().order_by('-id')
    return render(request,'staff_upadte_return_order.html',{"return_requests": return_requests})


def admin_update_order(request):
    if request.method == "POST":
        order_id = request.POST.get("order_id")
        new_status = request.POST.get("STATUS")
        order = Order.objects.filter(id=order_id).first()
        if order:
            order.STATUS = new_status
            order.save()
            if order.USER and hasattr(order.USER, 'LOGIN') and order.USER.LOGIN.email:
                send_mail(
                    subject="Your Order Status Updated",
                    message=f"Hello {order.USER.username},\n\n"
                            f"Your order #{order.id} status has been updated to: {new_status}.\n\n"
                            f"Thank you for shopping with us!",
                    from_email="yourgmail@gmail.com",
                    recipient_list=[order.USER.LOGIN.email],
                    fail_silently=False,
                )
        return redirect('admin_update_order')
    current_orders = Order.objects.exclude(STATUS__in=["Delivered", "Cancelled"]).order_by('-order_date')
    history_orders = Order.objects.filter(STATUS__in=["Delivered", "Cancelled"]).order_by('-order_date')
    status_options = ["Pending", "Confirmed", "Prepared", "Out for Delivery", "Delivered", "Cancelled"]
    return render(request, "admin_update_order.html", {"current_orders": current_orders,"history_orders": history_orders,"status_options": status_options})



def search(request):
    query = request.GET.get('q', '')
    fruits = Productfruits.objects.filter(name__icontains=query)
    snacks = Productsnacks.objects.filter(name__icontains=query)
    vegetables = Productvegitable.objects.filter(name__icontains=query)
    beverages = Productbeverages.objects.filter(name__icontains=query)
    egg = Productegg.objects.filter(name__icontains=query)
    fish = Productfish.objects.filter(name__icontains=query)
    rice = Productrice.objects.filter(name__icontains=query)
    milk = Productmilk.objects.filter(name__icontains=query)
    return render(request, "search.html", {"query": query,"fruits": fruits,"snaks":snacks,"vegetables":vegetables,"beverages":beverages,"egg":egg,"fish":fish,'rice':rice,'milk':milk})
        

        
def add_review(request,id):
    order_item_id=id
    user_id=request.session['user_id']
    if request.method=='POST':
        comment=request.POST['comment']
        rating=request.POST['rating']
        review=Review.objects.create(comment=comment,rating=rating,USER_id=user_id,ORDER_ITEM_id=order_item_id)
        review.save()
        return redirect('orders')
    return render(request, "add_review.html",{'order_item_id':order_item_id})



def bill(request, order_id):
    order = Order.objects.filter(id=order_id).first()
    if not order:
        return redirect("orders")
    user_id = request.session.get("user_id")
    if not request.user.is_superuser and order.USER.id != user_id:
        return redirect("orders")
    if order.STATUS != "Delivered":
        messages.error(request, "Bill will be available once the order is delivered.")
        return redirect("orders")
    order_items = OrderItem.objects.filter(ORDER=order)
    for item in order_items:
        item.subtotal = item.price * item.quantity
    total = sum(item.subtotal for item in order_items)
    return render(request, "bill.html", {"order": order,"order_items": order_items,"total": total})

