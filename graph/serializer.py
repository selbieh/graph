from rest_framework import serializers


class ConnectNodeSerializer(serializers.Serializer):
    start = serializers.CharField(required=True)
    end = serializers.CharField(required=False)
