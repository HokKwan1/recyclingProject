from rest_framework import serializers
from homepage.models import Request

class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = "__all__"  # Include all fields from the model