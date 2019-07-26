from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from interview.serializer import InterviewSerializer


class InterviewApi(APIView):
    serializer_class = InterviewSerializer

    def post(self, request, **kwargs):
        serializer = InterviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request, **kwargs):
        pass