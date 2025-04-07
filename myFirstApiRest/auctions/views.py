from django.shortcuts import render
from django.db.models import Q 

# Create your views here.
from rest_framework import generics 
from .models import Category, Auction, Bid
from .serializers import CategoryListCreateSerializer, CategoryDetailSerializer, AuctionListCreateSerializer, AuctionDetailSerializer , BidListCreateSerializer, BidDetailSerializer

class CategoryListCreate(generics.ListCreateAPIView): 
    queryset = Category.objects.all()  # Consulta base de datos (Qué devuelvo)
    serializer_class = CategoryListCreateSerializer  # Llamada al serializador (cómo lo devuelvo)

class CategoryRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView): 
    queryset = Category.objects.all() 
    serializer_class = CategoryDetailSerializer

class AuctionListCreate(generics.ListCreateAPIView): 
    queryset = Auction.objects.all() 
    serializer_class = AuctionListCreateSerializer 

    def get_queryset(self): 
        queryset = Auction.objects.all() 
        params = self.request.query_params 

        search = params.get('text', None) 
        if search: 
            queryset = queryset.filter(Q(title__icontains=search) | Q(description__icontains=search)) 
        
        category = params.get('category', None)
        if category:
            queryset = queryset.filter(Q(category__icontains=category))

        price_min = params.get('priceMin', None)
        if price_min:
            queryset = queryset.filter(price__gte=price_min)

        price_max = params.get('priceMax', None)
        if price_max:
            queryset = queryset.filter(price__lte=price_max)

        return queryset 

class AuctionRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView): 
    queryset = Auction.objects.all() 
    serializer_class = AuctionDetailSerializer

class BidListCreate(generics.ListCreateAPIView):
    # queryset = Bid.objects.all() 
    serializer_class = BidListCreateSerializer 

    def get_queryset(self):
        auction_id = self.kwargs["auction_id"]
        return Bid.objects.filter(auction_id=auction_id)
    
    def perform_create(self, serializer):
        auction_id = self.kwargs["auction_id"]
        serializer.save(auction_id=auction_id)

class BidRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Bid.objects.all() 
    serializer_class = BidDetailSerializer

    def get_queryset(self):
        auction_id = self.kwargs["auction_id"]
        return super().get_queryset().filter(auction_id=auction_id)