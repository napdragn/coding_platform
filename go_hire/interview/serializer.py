from rest_framework import serializers


class InterviewSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    creator_id = serializers.IntegerField()
    position = serializers.CharField()
