# reviews/views.py

from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from apps.restaurants.models import Restaurant
from apps.reviews.models import Review
from apps.reviews.serializers import ReviewSerializer, ReviewDetailSerializer


class ReviewListCreateView(ListCreateAPIView):
    queryset = Review.objects.all().order_by('-created_at')
    serializer_class = ReviewSerializer

    def get_queryset(self):
        restaurant_id = self.kwargs.get('restaurant_id')
        return self.queryset.filter(restaurant_id=restaurant_id)

    def perform_create(self, serializer):
        restaurant_id = self.kwargs.get('restaurant_id')
        # IntegrityError 방지.
        restaurant = get_object_or_404(Restaurant, id=restaurant_id)
        serializer.save(user=self.request.user, restaurant=restaurant)


class ReviewDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = ReviewDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return Review.objects.get(id=self.kwargs.get('review_id'), user=self.request.user)