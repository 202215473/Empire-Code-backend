from drf_spectacular.utils import extend_schema_field 
from rest_framework import serializers 
from datetime import timedelta
from django.utils import timezone
from .models import Category, Auction, Bid

class CategoryListCreateSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = Category  # A qué modelo hace referencia
        fields = ['id','name']  # Indico qué campos quiero


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
    
    def validate_closing_date(self, value): 
        if value < timezone.now() + timedelta(days=15): 
            raise serializers.ValidationError("La fecha de cierre debe ser al menos 15 días después de la fecha de creación") 
        return value 
     
class AuctionDetailSerializer(serializers.ModelSerializer): 
    creation_date = serializers.DateTimeField(format="%Y-%m%dT%H:%M:%SZ", read_only=True)  # Porque creation_date no se debería poder modificar
    closing_date = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%SZ") 
    isOpen = serializers.SerializerMethodField(read_only=True)  # Para evaluar si auction está abierta o no (es como un estado en react, pero aquí es más sencillo)

    class Meta: 
        model = Auction 
        fields = '__all__' 
 
    @extend_schema_field(serializers.BooleanField())
    def get_isOpen(self, obj):
        return obj.closing_date > timezone.now()

    def validate_closing_date(self, obj, value): 
        if value < obj.creation_date + timedelta(days=15): 
            raise serializers.ValidationError("La fecha de cierre debe ser al mneos 15 días después de la fecha de creación") 
        return value 
    
class BidListCreateSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = Bid 
        fields = '__all__' 

class BidDetailSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Bid 
        fields = '__all__' 