from django.shortcuts import render
from django.db.models import Q, Max
from django.utils import timezone

# Create your views here.
from rest_framework import generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

from .models import Category, Auction, Bid
from .serializers import CategoryListCreateSerializer, CategoryDetailSerializer, AuctionListCreateSerializer, AuctionDetailSerializer , BidListCreateSerializer, BidDetailSerializer
from .permissions import IsOwnerOrAdmin, IsNotAuctionOwner

class CategoryListCreate(generics.ListCreateAPIView): 
    permission_classes = [AllowAny]
    queryset = Category.objects.all()  # Consulta base de datos (Qué devuelvo)
    serializer_class = CategoryListCreateSerializer  # Llamada al serializador (cómo lo devuelvo)

class CategoryRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView): 
    permission_classes = [AllowAny]
    queryset = Category.objects.all() 
    serializer_class = CategoryDetailSerializer

class AuctionListCreate(generics.ListCreateAPIView): 
    queryset = Auction.objects.all() 
    serializer_class = AuctionListCreateSerializer 
    permission_classes = [AllowAny]

    def get_queryset(self): 
        queryset = Auction.objects.all() 
        params = self.request.query_params 

        search = params.get('text', None) 
        if search: 
            """if len(search) < 3:
                raise ValidationError( 
                    {"search": "La búsqueda debe tener al menos 3 caracteres."}, 
                    code=status.HTTP_400_BAD_REQUEST 
                )"""
            queryset = queryset.filter(Q(title__icontains=search) | Q(description__icontains=search)) 
        
        category = params.get('category', None)
        if category:
            if len(category) == 1:
                queryset = queryset.filter(Q(category__id__icontains=category))
            else:
                category_list = category.split(',')
                queryset = queryset.filter(category__id__in=category_list)

        price_min = params.get('priceMin', None)
        if price_min:
            queryset = queryset.filter(price__gte=price_min)

        price_max = params.get('priceMax', None)
        if price_max:
            queryset = queryset.filter(price__lte=price_max)

        return queryset 

class AuctionRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView): 
    permission_classes = [IsOwnerOrAdmin]
    queryset = Auction.objects.all() 
    serializer_class = AuctionDetailSerializer

class BidListCreate(generics.ListCreateAPIView):
    # queryset = Bid.objects.all() 
    serializer_class = BidListCreateSerializer
    permission_classes = [IsNotAuctionOwner]

    def get_queryset(self):
        auction_id = self.kwargs["auction_id"]
        return Bid.objects.filter(auction_id=auction_id)
    
    def perform_create(self, serializer):
        auction_id = self.kwargs["auction_id"]
        new_bid = serializer.validated_data["bid"]
        # new_bid = self.kwargs["bid"]
        # serializer.save(auction_id=auction_id)

        # VALIDATE IF BID IS OPEN
        auction = Auction.objects.get(id=auction_id)
        if auction.closing_date < timezone.now():
            raise ValidationError({"auction": f"La puja ya está cerrada (closing date: {auction.closing_date})."})

        # VALIDATE IF BID IS HIGHER THAN THE EXISTING BIDS
        max_bid = Bid.objects.filter(auction=auction).aggregate(Max("bid", default=-1))["bid__max"]
        if new_bid <= max_bid:
            raise ValidationError({"bid": f"La puja debe ser mayor que la puja actual más alta (${max_bid})."})
        auction.price = new_bid
        serializer.save(auction=auction)

class BidRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, IsNotAuctionOwner]
    queryset = Bid.objects.all() 
    serializer_class = BidDetailSerializer

    def get_queryset(self):
        auction_id = self.kwargs["auction_id"]
        return super().get_queryset().filter(auction_id=auction_id)
    
class UserAuctionListView(APIView): 
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs): 
        # Obtener las subastas del usuario autenticado 
        user_auctions = Auction.objects.filter(auctioneer=request.user) 
        serializer = AuctionListCreateSerializer(user_auctions, many=True) 
        return Response(serializer.data) 

class UserBidListView(APIView): 
    permission_classes = [IsAuthenticated] 
    def get(self, request, *args, **kwargs): 
        # Obtener las pujas del usuario autenticado 
        user_bids = Bid.objects.filter(username=request.user.username) 
        serializer = BidListCreateSerializer(user_bids, many=True) 
        return Response(serializer.data) 