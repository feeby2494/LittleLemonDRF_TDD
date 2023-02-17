from django.shortcuts import render
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView
# from rest_framework.response import Response

from .models import MenuItem
from .serializers import MenuItemSerializer

# Create your views here.
class MenuItemsView(ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    # def get(self, request):
    #     return Response({"message": "I work!"}, 200)
    
class SingleMenuItemView(RetrieveUpdateDestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer