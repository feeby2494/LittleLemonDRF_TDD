from .models import MenuItem
from rest_framework import serializers

class MenuItemSerializer(serializers.ModelSerializer):
    class Meta():
        model = MenuItem
        extra_kwargs = {'price' : {'min_value': 2}, 'inventory': {'min_value': 0}}
        fields = ['id', 'title', 'price', 'inventory']