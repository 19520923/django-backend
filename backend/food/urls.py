from unicodedata import name
from django.urls import path, re_path
from .views import FoodRateListView, OwnerFoodListView, FoodDetailView, FoodDeleteView, FoodSearchView,FoodRateDeleteView

urlpatterns = [
    path('food/food_list/', OwnerFoodListView.as_view(), name = 'food_list'),
    path('food/food_list/<int:id>', FoodDetailView.as_view(), name = 'food_detail'),
    path('food/food_delete/<int:id>', FoodDeleteView.as_view(), name = 'food_delete'),
    path('food/food_search/', FoodSearchView.as_view(), name = 'search'),
    path('food/food_rate/', FoodRateListView.as_view(), name = 'food_rate'),
    path('food/food_rate_delete/<int:id>', FoodRateDeleteView.as_view(), name = 'food_rate_delete'),
]