from drf_spectacular.utils import extend_schema_field 
from rest_framework import serializers 
from django.utils import timezone
from .models import Category, Auction, Bid

class CategoryListCreateSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = Category  # A qué modelo hace referencia
        fields = ['id','name']  # Indico qué campos quiero
    
    def validate_closing_date(self, value): 
        if value <= timezone.now(): 
            raise serializers.ValidationError("Closing date must be greater than now.") 
        return value 

class CategoryDetailSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = Category 
        fields = '__all__'  # Cuando quiero todos los campos

class AuctionListCreateSerializer(serializers.ModelSerializer): 
    creation_date = serializers.DateTimeField(format="%Y-%m%dT%H:%M:%SZ", read_only=True) 
    closing_date = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%SZ") 
    isOpen = serializers.SerializerMethodField(read_only=True) 
 
    class Meta: 
        model = Auction 
        fields = '__all__' 
 
    @extend_schema_field(serializers.BooleanField())
    def get_isOpen(self, obj): 
        return obj.closing_date > timezone.now() 
     
class AuctionDetailSerializer(serializers.ModelSerializer): 
    creation_date = serializers.DateTimeField(format="%Y-%m%dT%H:%M:%SZ", read_only=True)  # Porque creation_date no se debería poder modificar
    closing_date = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%SZ") 
    isOpen = serializers.SerializerMethodField(read_only=True)  # Para evaluar si auction está abierta o no (es como un estado en react, pero aquí es más sencillo)

    class Meta: 
        model = Auction 
        fields = '__all__' 
 
    @extend_schema_field(serializers.BooleanField())
    def get_isOpen(self, obj):
        print(obj.closing_date) 
        print(timezone.now())
        return obj.closing_date > timezone.now()

    def validate_closing_date(self, value): 
        if value <= timezone.now(): 
            raise serializers.ValidationError("Closing date must be greater than now, you idiot.") 
        return value 
    
class BidListCreateSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = Bid 
        fields = '__all__' 

class BidDetailSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Bid 
        fields = '__all__' 