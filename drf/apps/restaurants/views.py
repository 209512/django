# restaurants/views.py

from rest_framework.viewsets import ModelViewSet
from apps.restaurants.models import Restaurant
from apps.restaurants.serializers import RestaurantSerializer

class RestaurantViewSet(ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer