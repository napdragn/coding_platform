from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.utils import timezone

import json

from interview.serializer import InterviewSerializer
from interview.models import Interview, Round, Feedback


class InterviewApi(APIView):
    serializer_class = InterviewSerializer

    def post(self, request, **kwargs):
        data = json.loads(request.body)

        interview = Interview.objects.create(
            user_id=data.get('user_id'),
            creator_id=request.user.id,
            position=request.get('position'),
        )
        return Response({'interview_id': interview.id}, status=status.HTTP_201_CREATED)

    def get(self, request, pk, **kwargs):
        rounds = list(Round.objects.filter(interview_id=pk).values(
            'interviewee__username', 'start_time', 'type'
        ))
        return Response(rounds, status=status.HTTP_200_OK)


class RoundApi(APIView):
    serializer_class = InterviewSerializer

    def post(self, request, **kwargs):
        data = json.loads(request.body)
        round = Round.objects.create(
            interview_id=data.get('interview_id'),
            interviewee_id=data.get('interviewee_id'),
            start_time=timezone.datetime.strftime(data.get('start_time'),  "%Y-%m-%dt%H:%M"),
            type=data.get('type'),
        )
        return Response({'round_id': round.id}, status=status.HTTP_201_CREATED)

    def get(self, request, pk, **kwargs):
        feedback = list(Feedback.objects.filter(interview_round_id=pk).values(
            'query', 'feedback'
        ))
        return Response(feedback, status=status.HTTP_200_OK)


class FeedbackApi(APIView):
    serializer_class = InterviewSerializer

    def post(self, request, **kwargs):
        data = json.loads(request.body)
        feedback = Feedback.objects.create(
            interview_round_id=data.get('round_id'),
            query=data.get('query'),
            feedback=data.get('feedback')
        )
        return Response({'feedback_id': feedback.id}, status=status.HTTP_201_CREATED)

    def get(self, request, **kwargs):
        pass
