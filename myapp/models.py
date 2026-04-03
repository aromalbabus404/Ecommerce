from django.db import models


class Login(models.Model):
    email=models.EmailField(max_length=30)
    password=models.CharField(max_length=20)
    user_type=models.CharField(max_length=20)

    def __str__(self):
        return self.email
  

class User(models.Model):
    LOGIN=models.ForeignKey(Login,on_delete=models.CASCADE)
    username=models.CharField(max_length=20)
    firstname=models.CharField(max_length=20)
    lastname=models.CharField(max_length=20)
    phone=models.CharField(max_length=20)

    def __str__(self):
        return self.firstname

class Staff(models.Model):
    LOGIN=models.ForeignKey(Login,on_delete=models.CASCADE)
    username=models.CharField(max_length=20)
    firstname=models.CharField(max_length=20)
    lastname=models.CharField(max_length=20)
    dob=models.CharField(max_length=15)
    phone=models.IntegerField()
    image=models.ImageField(upload_to='gallery')

    def __str__(self):
        return self.firstname


class Productfruits(models.Model):
    image = models.ImageField(upload_to='products')
    stock = models.PositiveIntegerField(default=0)
    name = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now=True)
    available = models.BooleanField(default=True)
    kg = models.CharField(max_length=50, default='kg') 
    price = models.IntegerField()

    def __str__(self):
        return self.name


class Productsnacks(models.Model):
    image = models.ImageField(upload_to='products')
    stock = models.PositiveIntegerField(default=0)
    name = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now=True)
    available = models.BooleanField(default=True)
    price = models.IntegerField()

    def __str__(self):
        return self.name


class Productvegitable(models.Model):
    image = models.ImageField(upload_to='products')
    stock = models.PositiveIntegerField(default=0)
    name = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now=True)
    available = models.BooleanField(default=True)
    kg = models.CharField(max_length=50, default='kg') 
    price = models.IntegerField()

    def __str__(self):
        return self.name
    

class Productbeverages(models.Model):
    image = models.ImageField(upload_to='products')
    stock = models.PositiveIntegerField(default=0)
    name = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now=True)
    available = models.BooleanField(default=True)
    liter = models.CharField(max_length=20, default='liter')
    price = models.IntegerField()

    def __str__(self):
        return self.name   

class Productegg(models.Model):
    image = models.ImageField(upload_to='products')
    stock = models.PositiveIntegerField(default=0)
    name = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now=True)
    available = models.BooleanField(default=True)
    price = models.IntegerField(help_text="Price for one egg (in rupees)")

    def __str__(self):
        return self.name

class Productfish(models.Model):
    image = models.ImageField(upload_to='products')
    stock = models.PositiveIntegerField(default=0)
    name = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now=True)
    available = models.BooleanField(default=True)
    kg = models.CharField(max_length=50, default='kg')
    price = models.IntegerField()

    def __str__(self):
        return self.name

class Productrice(models.Model):
    image = models.ImageField(upload_to='products')
    stock = models.PositiveIntegerField(default=0)
    name = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now=True)
    available = models.BooleanField(default=True)
    kg = models.CharField(max_length=50, default='kg')
    price = models.IntegerField()
    
    def __str__(self):
        return self.name


class Productmilk(models.Model):
    image = models.ImageField(upload_to='products')
    stock = models.PositiveIntegerField(default=0)
    name = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now=True)
    available = models.BooleanField(default=True)
    litre = models.CharField(max_length=50, default='litre')
    price = models.IntegerField()
    
    def __str__(self):
        return self.name


class Cart(models.Model):
    USER = models.ForeignKey(User, on_delete=models.CASCADE)
    SNACKS = models.ForeignKey(Productsnacks, on_delete=models.CASCADE, null=True, blank=True)
    FRUITS = models.ForeignKey(Productfruits, on_delete=models.CASCADE, null=True, blank=True)
    VEGITABLES = models.ForeignKey(Productvegitable, on_delete=models.CASCADE, null=True, blank=True)
    BEVERAGES = models.ForeignKey(Productbeverages, on_delete=models.CASCADE, null=True, blank=True)
    EGGS = models.ForeignKey(Productegg, on_delete=models.CASCADE, null=True, blank=True)
    FISH = models.ForeignKey(Productfish, on_delete=models.CASCADE, null=True, blank=True)
    RICE = models.ForeignKey(Productrice, on_delete=models.CASCADE, null=True, blank=True)
    MILK = models.ForeignKey(Productmilk, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)



class Complaint(models.Model):
    USER = models.ForeignKey(User, on_delete=models.CASCADE)
    image=models.ImageField(upload_to='products')
    email=models.CharField(max_length=20)
    phone=models.IntegerField(max_length=10)
    category=models.CharField(max_length=20)
    subject=models.CharField(max_length=50)

    def __str__(self):
        return self.email
    

class Response(models.Model):
    USER = models.ForeignKey(User, on_delete=models.CASCADE)
    responder=models.CharField(max_length=30)
    response=models.CharField(max_length=50)
    status=models.CharField(max_length=20)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.responder
       

class Address(models.Model):
    USER = models.ForeignKey(User, on_delete=models.CASCADE) 
    fullname = models.CharField(max_length=200)
    phone = models.CharField(max_length=10)
    district = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    housename = models.CharField(max_length=200)
    landmark = models.CharField(max_length=200)
    state = models.CharField(max_length=10)
    pincode = models.CharField(max_length=10) 

    def __str__(self):
        return self.fullname


STATUS_CHOICES = (
    ("Pending", "Pending"),
    ("Prepared", "Prepared"),
    ("Confirmed", "Confirmed"),
    ("Out for Delivery", "Out for Delivery"),
    ("Delivered", "Delivered"),
    ("Cancelled", "Cancelled"),
)



class Order(models.Model):
    USER = models.ForeignKey(User, on_delete=models.CASCADE)
    ADDRESS = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True)
    payment_method = models.CharField(max_length=50)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    STATUS = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Pending")
    order_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - {self.USER.username}"


class OrderItem(models.Model):
    ORDER = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    SNACKS = models.ForeignKey(Productsnacks, on_delete=models.CASCADE, null=True, blank=True)
    FRUITS = models.ForeignKey(Productfruits, on_delete=models.CASCADE, null=True, blank=True)
    VEGITABLES = models.ForeignKey(Productvegitable, on_delete=models.CASCADE, null=True, blank=True)
    BEVERAGES = models.ForeignKey(Productbeverages, on_delete=models.CASCADE, null=True, blank=True)
    EGGS = models.ForeignKey(Productegg, on_delete=models.CASCADE, null=True, blank=True)
    FISH = models.ForeignKey(Productfish, on_delete=models.CASCADE, null=True, blank=True)
    RICE = models.ForeignKey(Productrice, on_delete=models.CASCADE, null=True, blank=True)
    MILK = models.ForeignKey(Productmilk, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        product = self.SNACKS or self.FRUITS or self.VEGITABLES or self.BEVERAGES \
                  or self.EGGS or self.FISH or self.RICE or self.MILK
        return f"{product} x {self.quantity} (${self.price})"
    


class ReturnRequest(models.Model):
    STATUS_CHOICES = (
        ("Requested", "Requested"),
        ("Pickup Scheduled", "Pickup Scheduled"),
        ("Picked Up", "Picked Up"),
        ("Approved", "Approved"),
        ("Rejected", "Rejected"),
        ("Refunded", "Refunded"),
    )

    ORDER_ITEM = models.ForeignKey(OrderItem, on_delete=models.CASCADE)
    reason = models.TextField()
    status = models.CharField(max_length=20, default="Requested")
    request_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Return for OrderItem {self.ORDER_ITEM.id}"





class Review(models.Model):
    USER = models.ForeignKey(User, on_delete=models.CASCADE)
    ORDER_ITEM=models.ForeignKey(OrderItem,on_delete=models.CASCADE,related_name='reviews')
    comment=models.CharField(max_length=100)
    rating = models.CharField(max_length=5)

    def __str__(self):
        return self.comment