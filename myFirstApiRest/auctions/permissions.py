
from rest_framework.permissions import BasePermission, SAFE_METHODS 
from auctions.models import Auction, Comment

class IsOwnerOrAdmin(BasePermission): 
    """ 
    Permite editar/eliminar una subasta solo si el usuario es el propietario 
    o es administrador. Cualquiera puede consultar (GET). 
    """ 
 
    def has_object_permission(self, request, view, obj): 
        # Permitir acceso de lectura a cualquier usuario (GET, HEAD, OPTIONS) 
        if request.method in SAFE_METHODS: 
            return True 
 
        # Permitir si el usuario es el creador o es administrador 
        try:
            return obj.auctioneer == request.user or request.user.is_staff
        except AttributeError:
            return obj.user == request.user or request.user.is_staff


class IsNotAuctionOwner(BasePermission): 
    """ 
    Permite crear puja de una subasta solo si el usuario NO es el propietario. 
    Cualquiera puede consultar (GET).
    """ 
 
    def has_permission(self, request, view): 
        # Permitir acceso de lectura a cualquier usuario (GET, HEAD, OPTIONS) 
        auction_id = view.kwargs.get("auction_id")
        if not auction_id:
            return False
        else:
            auction = Auction.objects.get(id=auction_id)

        if request.method in SAFE_METHODS: 
            return True

        if request.user:
            return auction.auctioneer.username != request.user.username or request.user.is_staff

        return False

class IsCommentOwnerOrAdmin(BasePermission): 
    """ 
    Permite editar/eliminar una subasta solo si el usuario es el propietario 
    o es administrador. Cualquiera puede consultar (GET). 
    """ 
 
    def has_permission(self, request, view): 
        auction_id = view.kwargs.get("auction_id")
        if not auction_id:
            return False
        else:
            auction = Auction.objects.get(id=auction_id)
            comments = Comment.objects.filter(auction=auction, user=request.user)

        if request.method in SAFE_METHODS: 
            return True

        if request.user:
            # return comment.user.username == request.user.username or request.user.is_staff
            return len(comments) > 0 or request.user.is_staff

        return False
