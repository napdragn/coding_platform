from rest_framework import serializers


class GetContestsSerializer(serializers.Serializer):
    pass


class GetContestQuestionsSerializer(serializers.Serializer):
    contest_id = serializers.CharField()