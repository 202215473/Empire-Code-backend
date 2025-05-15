from django.urls import path 
from .views import CategoryListCreate, CategoryRetrieveUpdateDestroy, AuctionListCreate, AuctionRetrieveUpdateDestroy, BidListCreate, BidRetrieveUpdateDestroy, CommentListCreate, CommentRetrieveUpdateDestroy, RatingListCreate, RatingRetrieveUpdateDestroy

app_name="auctions" 
urlpatterns = [ 
    path('categories/', CategoryListCreate.as_view(), name='category-list-create'),  # protegido con permisos
    path('categories/<int:pk>/', CategoryRetrieveUpdateDestroy.as_view(), name='category-detail'),  # protegido con permisos
    path('', AuctionListCreate.as_view(), name='auction-list-create'),  # protegido con permisos
    path('<int:pk>/', AuctionRetrieveUpdateDestroy.as_view(), name='auction-detail'),  # este está proegido por permisos
    path('<int:auction_id>/bids/', BidListCreate.as_view(), name='bid-list-create'),  # protegido con permisos
    path('<int:auction_id>/bids/<int:pk>/', BidRetrieveUpdateDestroy.as_view(), name='bid-detail'),  # protegido con permisos
    path('<int:auction_id>/comments/', CommentListCreate.as_view(), name='bid-list-create'),  # protegido con permisos
    path('<int:auction_id>/comments/<int:pk>/', CommentRetrieveUpdateDestroy.as_view(), name='comment-detail'),  # protegido con permisos
    path('<int:auction_id>/ratings/', RatingListCreate.as_view(), name='rating-list-create'),
    path('<int:auction_id>/ratings/<int:pk>/', RatingRetrieveUpdateDestroy.as_view(), name='rating-detail'),
] 