from rest_framework import serializers


class GetContestsSerializer(serializers.Serializer):
    pass


class BeginContestSerializer(serializers.Serializer):
    contest_id = serializers.CharField()


class SubmitContestSerializer(serializers.Serializer):
    pass
