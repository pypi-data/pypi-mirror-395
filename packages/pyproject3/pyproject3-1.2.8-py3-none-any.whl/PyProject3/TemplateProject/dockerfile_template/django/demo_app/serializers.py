

from rest_framework import serializers


class ChatMessageSerializer(serializers.Serializer):
    role = serializers.CharField()
    content = serializers.CharField()


class ChatCompletionSerializer(serializers.Serializer):
    model = serializers.CharField()
    messages = ChatMessageSerializer(many=True)
    temperature = serializers.FloatField(default=0.7)
    timeout = serializers.IntegerField(default=30)