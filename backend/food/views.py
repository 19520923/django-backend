from django.http import Http404
from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView, DestroyAPIView, ListAPIView
from .serializers import FoodRateSerializer, FoodSerializer
from .models import Food, FoodRate, Ingredient
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwner
from rest_framework.response import Response
from rest_framework import status

# Create your views here.
class OwnerFoodListView(ListCreateAPIView):
    serializer_class = FoodSerializer
    queryset = Food.objects.all()
    permission_classes = [IsAuthenticated,]
    
    def perform_create(self, serializer):
        return serializer.save(author = self.request.user)
    
    def get_queryset(self):
        return self.queryset.filter(author = self.request.GET['author_id']).order_by('-create_at')
    
    
class FoodDetailView(RetrieveAPIView):
    serializer_class = FoodSerializer
    queryset = Food.objects.all()
    permission_classes = [IsAuthenticated,]
    lookup_field = 'id'
    
    def get_queryset(self):
        return self.queryset.all()
    
class FoodDeleteView(DestroyAPIView):
    serializer_class = FoodSerializer
    queryset = Food.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]
    lookup_field = 'id'
    
    def get_queryset(self):
        return self.queryset.filter(author = self.request.user)
    
    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response({'message': 'Deleted'}, status = status.HTTP_200_OK)
        except Http404: 
            return Response(status=status.HTTP_204_NO_CONTENT)
        
class FoodSearchView(ListAPIView):
    serializer_class = FoodSerializer
    queryset = Food.objects.all()
    permission_classes = [IsAuthenticated,]
    
    def get_queryset(self):
        return self.queryset.filter(name__icontains = self.request.GET['search']).order_by('-avg_score', '-create_at')
    
class FoodRateListView(ListCreateAPIView):
    serializer_class = FoodRateSerializer
    queryset = FoodRate.objects.all()
    permission_classes = [IsAuthenticated,]
    
    def perform_create(self, serializer):
        return serializer.save(author = self.request.user, food = Food.objects.get(pk = self.request.GET['id']))
    
    def get_queryset(self):
        return self.queryset.filter(food = self.request.GET['id']).order_by('-create_at')
    
class FoodRateDeleteView(DestroyAPIView):
    serializer_class = FoodRateSerializer
    queryset = FoodRate.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]
    lookup_field = 'id'
    
    def get_queryset(self):
        return self.queryset.filter(author = self.request.user)
    
    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response({'message': 'Deleted'}, status = status.HTTP_200_OK)
        except Http404: 
            return Response(status=status.HTTP_204_NO_CONTENT)