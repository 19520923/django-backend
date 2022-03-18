from asyncio.windows_events import NULL
from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwner
from django.db.models import Q

from .models import Post, PostComment, Reaction

from .serializers import PostCommentSerializer, PostSerializer, ReactionSerializer
# Create your views here.

class PostListView(generics.ListCreateAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    permission_classes = [IsAuthenticated,]
    
    def perform_create(self, serializer):
        return serializer.save(author = self.request.user)
    
    def get_queryset(self):
        return self.queryset.filter(is_public = True).order_by('-create_at')
    
class PostTimeLineView(generics.ListAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        author = self.request.GET['id']
        user = self.request.user
        if author == user:        
            return self.queryset.filter(author = self.request.GET['id']).order_by('-create_at')
        else:
            return self.queryset.filter(author = self.request.GET['id'], is_public = True).order_by('-create_at')

class PostDetailView(generics.RetrieveDestroyAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'
    
    def get_queryset(self):
        return self.queryset.all()
    
    
class CommentListView(generics.ListCreateAPIView):
    serializer_class = PostCommentSerializer
    queryset = PostComment.objects.all()
    permission_classes = [IsAuthenticated,]
    
    def perform_create(self, serializer):
        return serializer.save(author = self.request.user)
    
    def get_queryset(self):
        return self.queryset.filter(post = self.request.GET['id'], parent__isnull = True).order_by('-create_at')
    

class CommentDeleteView(generics.DestroyAPIView):
    serializer_class = PostCommentSerializer
    queryset = PostComment.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]
    lookup_field = 'id'
    
    def get_queryset(self):
        return self.queryset.all()
    
    
class ReactionListView(generics.ListCreateAPIView):
    erializer_class = ReactionSerializer
    queryset = Reaction.objects.all()
    permission_classes = [IsAuthenticated,]
    
    def perform_create(self, serializer):
        return serializer.save(author = self.request.user,
                               post = self.request.GET['id'])
    
    def get_queryset(self):
        return self.queryset.filter(post = self.request.GET['id']).order_by('-create_at')
    
class ReactionDeleteView(generics.DestroyAPIView):
    serializer_class = ReactionSerializer
    queryset = Reaction.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]
    lookup_field = 'id'
    
    def get_queryset(self):
        return self.queryset.all()