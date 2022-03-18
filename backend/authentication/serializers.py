from rest_framework import serializers

from .models import User, UserFollow
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=8, write_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name']
        
    def validate(self, attrs):
        email = attrs['email']
        username = attrs['password']
        first_name_mod = attrs['first_name'].split(' ')
        last_name_mod = attrs['last_name'].split(' ')
        if not username.isalnum():
            raise serializers.ValidationError('The username should only contain alphanumeric characters')
        for first_name in first_name_mod:
            if not first_name.isalpha():
                raise serializers.ValidationError('The name should only contain alphabet characters')
            
        for last_name in last_name_mod:
            if not last_name.isalpha():
                raise serializers.ValidationError('The name should only contain alphabet characters')
        return attrs
    
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    
class VerifyEmailSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        model = User
        fields = ['token']
        
        
class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=3)
    password = serializers.CharField(max_length=255, min_length=8, write_only = True)
    username = serializers.CharField(max_length=255, read_only=True)
    tokens = serializers.CharField(max_length=255, read_only=True)
    
    class Meta:
        model = User
        fields = ['email', 'password', 'username', 'tokens']
    
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        
        user = auth.authenticate(email=email, password=password)
        
        if not user:
            raise AuthenticationFailed('Invalid credentials, try again')
        
        if not user.is_active:
            raise AuthenticationFailed('Account disabled, please contact administrator')
        
        if not user.is_verified:
            raise AuthenticationFailed('Email is not verified')
        
        
        return {
            'email': user.email,
            'username': user.username,
            'tokens': user.tokens()
        }
        
class UserSerializer(serializers.ModelSerializer):
    
    
    class Meta:
        model = User
        fields = ['username','email','first_name','last_name','is_current','create_at', 'last_login', 'avatar_url', 'cover_url', 'about']
        extra_kwargs = {'is_current': {'read_only': True},
                        'create_at': {'read_only': True},
                        'email': {'read_only': True},
                        'last_login': {'read_only': True},}
        
        
        def validate(self, attrs):
            email = attrs['email']
            username = attrs['password']
            first_name_mod = attrs['first_name'].split(' ')
            last_name_mod = attrs['last_name'].split(' ')
            if not username.isalnum():
                raise serializers.ValidationError('The username should only contain alphanumeric characters')
            for first_name in first_name_mod:
                if not first_name.isalpha():
                    raise serializers.ValidationError('The name should only contain alphabet characters')
                
            for last_name in last_name_mod:
                if not last_name.isalpha():
                    raise serializers.ValidationError('The name should only contain alphabet characters')
            return attrs
     
class UserFollowSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = UserFollow
        fields = '__all__'
        
    def validate(self, attrs):
        user = User.objects.get(pk = attrs)
        if not user:
            raise serializers.ValidationError('User not exists')
        if not user.is_active:
            raise serializers.ValidationError('User unactivate')
        if not user.is_verified:
            raise serializers.ValidationError('User not verified')
        return attrs


    
    