from django.urls import path 
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView) 

from .views import UserRegisterView, UserListView, UserRetrieveUpdateDestroyView, UserProfileView, ChangePasswordView, LogoutView, CurrentUserView
from auctions.views import UserAuctionListView, UserBidListView
 
app_name="users" 
urlpatterns = [ 
    path('register/', UserRegisterView.as_view(), name='user-register'),  # protegido con permisos
    path('', UserListView.as_view(), name='user-list'),  # protegido con permisos
    path('<int:pk>/', UserRetrieveUpdateDestroyView.as_view(), name='user-detail'), 
    path('profile/', UserProfileView.as_view(), name='user-profile'),  # protegido con permisos
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),  # protegido con permisos
    path('log-out/', LogoutView.as_view(), name='log-out'),  # protegido con permisos
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('my-auctions/', UserAuctionListView.as_view(), name='user-auctions'),  # protegido con permisos
    path('my-bids/', UserBidListView.as_view(), name='user-auctions'),  # protegido con permisos
    path('me/', CurrentUserView.as_view(), name='current-user'),
]