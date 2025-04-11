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
    rating = models.DecimalField(max_digits=3, decimal_places=2, validators=[MinValueValidator(Decimal('1.00')), MaxValueValidator(Decimal('5.00'))]) 
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
    bid = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('1.00'))]) 
    creation_date = models.DateTimeField(auto_now_add=True)
    username = models.CharField(max_length=150)
 
    class Meta:  
        ordering=('auction', 'bid')  
 
    def __str__(self): 
        return f"Bid of auction {self.auction} for {self.bid}$"
    