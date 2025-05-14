from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal
from users.models import CustomUser 

class Category(models.Model): 
    name = models.CharField(max_length=50, blank=False, unique=True) 
 
    class Meta:  
        ordering=('id',)  
 
    def __str__(self): 
        return self.name 
 
class Auction(models.Model): 
    title = models.CharField(max_length=150) 
    description = models.TextField() 
    price = models.IntegerField(validators=[MinValueValidator(1)])
    brand = models.CharField(max_length=100) 
    category = models.ForeignKey(Category, related_name='auctions', on_delete=models.CASCADE)
    thumbnail = models.URLField()
    creation_date = models.DateTimeField(auto_now_add=True)
    closing_date = models.DateTimeField() 
    stock = models.IntegerField(validators=[MinValueValidator(1)])

    auctioneer = models.ForeignKey(CustomUser, related_name='auctions', on_delete=models.CASCADE) 

    # En la consulta de shell, si quiero que la fecha se muestre bonita hay que pasarla 
    # como .strtime(format=<formato_fecha_deseado>)
    class Meta:  
        ordering=('id',)
 
    def __str__(self): 
        return self.title 

# get_queryset
# Redefiniendo un poco la parte de listar en BidListCreate
# Capturamos el parámetro que queremos.

class Bid(models.Model):
    auction = models.ForeignKey(Auction, related_name='bids', on_delete=models.CASCADE) 
    bid = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('1.00'))])  # precio de la puja
    creation_date = models.DateTimeField(auto_now_add=True)
    username = models.CharField(max_length=150)  # no es ForeignKey porque no quieres poder acceder al usuario dessde la puja
 
    class Meta:  
        ordering=('auction', 'bid')  # id compuesto
 
    def __str__(self): 
        return f"Bid of auction {self.auction} for {self.bid}$"
    
class Rating(models.Model):
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    user = models.ForeignKey(CustomUser, related_name='ratings', on_delete=models.CASCADE) 
    auction = models.ForeignKey(Auction, related_name='ratings', on_delete=models.CASCADE)
    
    class Meta:  
        ordering=('auction', 'rating')  # id compuesto

    def __str__(self): 
        return f"Rating of auction {self.auction} of {self.rating} by {self.user}"

class Comment(models.Model):
    auction = models.ForeignKey(Auction, related_name="comments", on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, related_name="comments", on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    text = models.TextField(blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)  # auto_now_add edits the field ONLY the first time i use it
    last_modified = models.DateTimeField(auto_now=True)  # auto_now updates every time we save a comment

    class Meta:
        ordering=('auction', 'user', 'creation_date')
    
    def __str__(self):
        return f"Comment for auction {self.auction} with id {self.id}"