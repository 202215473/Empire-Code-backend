from rest_framework import serializers 
from .models import CustomUser

class UserSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = CustomUser 
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'birth_date', 'municipality','locality', 'password') 
        extra_kwargs = { 
            'password': {'write_only': True},  # Así no se puede mostrar nunca la contraseña
        } 

    def validate_email(self, value): 
        user = self.instance  # Solo tiene valor cuando se está actualizando 
        if CustomUser.objects.filter(email=value).exclude(pk=user.pk if user else None).exists(): 
            raise serializers.ValidationError("Email already in used.") 
        return value 
    
    def create(self, validated_data): 
        return CustomUser.objects.create_user(**validated_data)
    
class MinimalUserSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = CustomUser 
        fields = ('id', 'username') 

class ChangePasswordSerializer(serializers.Serializer): 
    old_password = serializers.CharField(required=True) 
    new_password = serializers.CharField(required=True) 