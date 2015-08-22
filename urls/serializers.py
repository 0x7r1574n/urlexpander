from rest_framework import serializers
from .models import Url


class UrlSerializer(serializers.ModelSerializer):
    origin = serializers.URLField(required=True)
    destination = serializers.URLField(required=False)
    status = serializers.IntegerField(required=False)
    title = serializers.CharField(max_length=200, required=False, allow_blank=True)
    screenshot = serializers.URLField(required=False)

    class Meta:
        model = Url
        fields = ('origin', 'destination', 'status', 'title', 'screenshot')
        read_only_fields = ('destination', 'status', 'title', 'screenshot')
