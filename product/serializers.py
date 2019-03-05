from rest_framework import serializers
from product.models import product


class ProductSerializer(serializers.ModelSerializer):
	class Meta:
		model = product
		fields = "__all__"