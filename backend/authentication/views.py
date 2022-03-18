from django.shortcuts import render
from rest_framework import generics
from .serializers import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User, UserFollow
from .utils import Utils
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
import jwt
from django.conf import settings
from django.contrib.auth import logout
import datetime
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwner
# Create your views here.

class RegisterView(generics.GenericAPIView):
    def post(self, request):
        user = request.data
        serializer = RegisterSerializer(data=user)
        serializer.is_valid(raise_exception = True)
        serializer.save()
        user_data = serializer.data
        user = User.objects.get(email=user_data['email'])
        token = RefreshToken.for_user(user).access_token
        
        current_site = get_current_site(request).domain
        relativeLink = reverse('email-verify')
        absurl = 'http://' + current_site + relativeLink + "?token="+ str(token)
        email_body = 'Hi ' + user.username + ',\nUse link below to verify your account\n' + absurl
        
        data = {
            'email_subject': 'Verify your email',
            'email_body': email_body,
            'to_email': user.email,
        }
        
        Utils.send_email(data)
        
        return Response(user_data, status = status.HTTP_201_CREATED)


class VerifyEmailView(generics.GenericAPIView):
    serializer_class = VerifyEmailSerializer
    
    def get(self, request):
        token = request.GET['token']
        try:
            payload = jwt.decode(jwt = token, key = settings.SECRET_KEY, algorithms=['HS256'])
            user = User.objects.get(pk=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()
            
            return Response({'message': 'Successfully activated'}, status= status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as identifier:
            return Response({'error': 'Activation Expired'}, status = status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            return Response({'error': payload}, status = status.HTTP_400_BAD_REQUEST)

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception = True)
        data = serializer.data
        user = User.objects.get(email = data['email'])
        if user:
            user.last_login = datetime.datetime.now()
            user.is_current = True
            user.save()
        
        return Response(data, status=status.HTTP_200_OK)
    

class LogoutView(generics.GenericAPIView):
    def post(self, request):
        logout(request)
        
        return Response({'message': 'Logout successfully'}, status = status.HTTP_200_OK)
    
    
    
class UserSearchListView(generics.ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated,]
    
    def get_queryset(self):
        return self.queryset.filter(username__icontains = self.request.GET['search'],
                                    is_active = True,
                                    is_verified = True).order_by('username')
    
    
class UserDetailView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated,]
    lookup_field = 'id'
    
    def get_queryset(self):
        return self.queryset.all()
    
class UserUpdateView(generics.UpdateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'
    
    def get_queryset(self):
        return self.queryset.all()
    

class UserUnactiveView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        user = User.objects.get(email = request.user)
        if user:
            user.is_active = False
            user.save()
            return Response({'message': 'Account has been unactivated'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Something went wrong'}, status=status.HTTP_400_BAD_REQUEST)
        
        
class UserFollowerListView(generics.ListCreateAPIView):
    serializer_class = UserFollowSerializer
    queryset = UserFollow.objects.all()
    permission_classes = [IsAuthenticated,]
    
    def get_queryset(self):
        return self.queryset.filter(user = self.request.user)
    
    def perform_create(self, serializer):
        return serializer.save(user = self.request.POST['id'], 
                               follower =  self.request.user)
    
class UnfollowView(generics.DestroyAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return self.queryset.filter(follower = self.request.user, user = self.request.DELETE['id'])