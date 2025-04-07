from django.db import models

# Create your models here.

from django.db import models 
from django.core.validators import MinValueValidator 

"""
from auctions.models import Category,Auction 
from django.utils import timezone 
from datetime import timedelta 
 
categ = Category.objects.get(id=2)   
 
auction = Auction( 
    title="Laptop Gamer ASUS", 
    description="Laptop gamer con RTX 3060 y 16GB RAM.", 
    price=1500.00, 
    rating=4.8, 
    stock=10, 
    brand="ASUS", 
    category=categ, 
    thumbnail="https://dlcdnwebimgs.asus.com/gain/3D241166-0518-4745B481-D901886BFD14", 
    closing_date=timezone.now() + timedelta(days=16)  
) 
 
auction.full_clean() #Comando que ejecuta las validaciones  
auction.save()
"""


class Category(models.Model): 
    name = models.CharField(max_length=50, blank=False, unique=True) 
 
    class Meta:  
        ordering=('id',)  
 
    def __str__(self): 
        return self.name 
 
class Auction(models.Model): 
    title = models.CharField(max_length=150) 
    description = models.TextField() 
    price = models.DecimalField(max_digits=10, decimal_places=2) 
    rating = models.DecimalField(max_digits=3, decimal_places=2) 
    # stock = models.IntegerField
    brand = models.CharField(max_length=100) 
    # ForeingKey indica la relación ya (ver apuntes)
    category = models.ForeignKey(Category, related_name='auctions', on_delete=models.CASCADE)
    thumbnail = models.URLField()
    # Este campo no lo pasamos pero con la propiedad auto_now_add lo que pasa es que 
    # creation_date solo la puede crear la base de datos, pero no se puede modificar 
    # nunca y por ello no necesitamos pasársela al crear una Auction
    creation_date = models.DateTimeField(auto_now_add=True)      
    closing_date = models.DateTimeField() 
    stock = models.IntegerField(validators=[MinValueValidator(1)])

# En la consulta de shell, si quiero que la fecha se muestre bonita hay que pasarla 
# como .strtime(format=<formato_fecha_deseado>)
    class Meta:  
        ordering=('id',)  
        # No siempre te interesa ordenar por ID, en el caso de la subasta se podría ordenar por id y precio, por ejemplo (tendría id compuesto)
 
    def __str__(self): 
        return self.title 

# get_queryset
# Redefiniendo un poco la parte de listar en BidListCreate
# Capturamos el parámetro que queremos.

class Bid(models.Model):
    auction = models.ForeignKey(Auction, related_name='bids', on_delete=models.CASCADE) 
    bid = models.DecimalField(max_digits=10, decimal_places=2) 
    creation_date = models.DateTimeField(auto_now_add=True)
    # username = models.CharField(max_length=150)
 
    class Meta:  
        ordering=('auction', 'bid')  
 
    def __str__(self): 
        return f"Bid of auction {self.auction} for {self.bid}$"
    