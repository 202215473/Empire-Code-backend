from drf_spectacular.utils import extend_schema_field 
from rest_framework import serializers 
from datetime import timedelta
from django.utils import timezone
from .models import Category, Auction, Bid, Rating
from django.db.models import Avg

class CategoryListCreateSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = Category  # A qué modelo hace referencia
        fields = ['id','name']  # Indico qué campos quiero


class CategoryDetailSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = Category 
        fields = '__all__'  # Cuando quiero todos los campos

class AuctionListCreateSerializer(serializers.ModelSerializer): 
    creation_date = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%SZ", read_only=True) 
    closing_date = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%SZ") 
    isOpen = serializers.SerializerMethodField(read_only=True) 
    rating = serializers.SerializerMethodField(read_only=True) 

    class Meta: 
        model = Auction 
        fields = '__all__' 
        read_only_fields = ['auctioneer', 'creation_date']

    def create(self, validated_data):
        validated_data['auctioneer'] = self.context['request'].user
        return super().create(validated_data)
 
    @extend_schema_field(serializers.BooleanField())
    def get_isOpen(self, obj): 
        return obj.closing_date > timezone.now() 
    
    @extend_schema_field(serializers.DecimalField(max_digits=3, decimal_places=2))
    def get_rating(self, obj): 
        rating = obj.ratings.aggregate(avg_rating=Avg('rating'))['avg_rating']
        return round(rating, 2) if rating else 1.0
    
    def validate_closing_date(self, value): 
        if value < timezone.now() + timedelta(days=15): 
            raise serializers.ValidationError("La fecha de cierre debe ser al menos 15 días después de la fecha de creación") 
        return value 
     
class AuctionDetailSerializer(serializers.ModelSerializer): 
    creation_date = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%SZ", read_only=True)  # Porque creation_date no se debería poder modificar
    closing_date = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%SZ") 
    isOpen = serializers.SerializerMethodField(read_only=True)  # Para evaluar si auction está abierta o no (es como un estado en react, pero aquí es más sencillo)
    rating = serializers.SerializerMethodField(read_only=True) 

    class Meta: 
        model = Auction 
        fields = '__all__' 
        read_only_fields = ['auctioneer', 'creation_date']
 
    @extend_schema_field(serializers.BooleanField())
    def get_isOpen(self, obj):
        return obj.closing_date > timezone.now()
    
    @extend_schema_field(serializers.DecimalField(max_digits=3, decimal_places=2))
    def get_rating(self, obj): 
        rating = obj.ratings.aggregate(avg_rating=Avg('rating'))['avg_rating']
        return round(rating, 2) if rating else 1.0

    def validate_closing_date(self, value): 
        creation_date = self.instance.creation_date
        if value < creation_date + timedelta(days=15): 
            raise serializers.ValidationError("La fecha de cierre debe ser al menos 15 días después de la fecha de creación") 
        return value 
    
class BidListCreateSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = Bid 
        fields = '__all__' 

    def create(self, validated_data):
        auction = validated_data['auction']
        bid_price = validated_data['bid']
        bid = Bid.objects.create(**validated_data)  # le pasa key=value de cada elemento de validated_data (que es un dict)
        if bid_price > auction.price:  # se debería cumplir siempre
            auction.price = bid_price
            auction.save()  # Guardamos los cambios en la subasta
        else:
            print(f"no se ha guardado la subasta porque {bid_price} !> {auction.price}")
        return bid
    # def validate_auction(self, obj):
    #     isOpen = obj.auction.get_isOpen()
    
    # def validate_bid(self, obj):
    #     new_bid = obj.bid
    #     max_bid = Bid.objects.aggregate(Max("bid", default=1))
        
    #     if new_bid <= max_bid:
    #         raise serializers.ValidationError(f"La puja debe ser mayor que la puja máxima actual de {max_bid} $")
        
    #     return obj
    
    # def validate_bid(self, value):
    #     max_bid = Bid.objects.aggregate(Max("bid", default=1))
        
    #     if value <= max_bid:
    #         raise serializers.ValidationError(f"La puja debe ser mayor que la puja máxima actual de {max_bid} $")
        
    #     return value


class BidDetailSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Bid 
        fields = '__all__' 


class RatingListCreateSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Rating 
        fields = '__all__' 
        read_only_fields = ['user', 'auction']

    def create(self, validated_data):
        user = self.context['request'].user
        auction = self.context['auction']

        if Rating.objects.filter(user=user, auction=auction).exists():
            raise serializers.ValidationError("You have already rated this auction.")
        else:
            return super().create(validated_data)
    

class RatingDetailSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Rating 
        fields = '__all__' 
        read_only_fields = ['user', 'auction']