import datetime
import json

from contests.models import Contest, ContestQuestionMapping, UserContest
from contests.serializer import BeginContestSerializer, GetContestsSerializer
from question.models import Answer, Question, QuestionTagMapping, Tag
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView


class GetContestsApi(APIView):
    serializer_class = GetContestsSerializer

    def post(self, request, **kwargs):
        pass

    def get(self, request, **kwargs):
        if not request.user.is_authenticated:
            resp_dict = {
                "success": False,
                "error_message": "User not authenticated, Please Login."
            }
            return Response(resp_dict, status=status.HTTP_200_OK)
        email = request.user.username
        user_contest_list = UserContest.objects.filter(
            email=email,
            user_start_time__isnull=True
        ).values_list('contest_id', flat=True)
        contest_title_mapping = list()
        for contest_id in user_contest_list:
            contest_title = Contest.objects.get(id=contest_id).title
            contest_title_mapping.append({
                "contest_id": contest_id,
                "contest_title": contest_title
            })
        resp_dict = {
            "success": True,
            "active_contests": contest_title_mapping
        }
        return Response(resp_dict, status=status.HTTP_200_OK)


class BeginContestApi(APIView):
    serializer_class = BeginContestSerializer

    def post(self, request, **kwargs):
        if not request.user.is_authenticated:
            resp_dict = {
                "success": False,
                "error_message": "User not authenticated, Please Login."
            }
            return Response(resp_dict, status=status.HTTP_200_OK)
        post_data = json.loads(request.data)
        email = request.user.username
        contest_id = post_data.get('contest_id', '')
        if not contest_id:
            resp_dict = {
                "success": False,
                "error_message": "Missing contest_id"
            }
            return Response(resp_dict, status=status.HTTP_200_OK)
        user_contest_obj = UserContest.objects.filter(
            contest_id=contest_id,
            email=email,
            user_start_time__isnull=True
        )
        if not user_contest_obj:
            resp_dict = {
                "success": False,
                "error_message": "Unable to find any untaken contests."
            }
            return Response(resp_dict, status=status.HTTP_200_OK)
        user_contest_obj.user_start_time = datetime.datetime.now()
        contest_question_id_list = ContestQuestionMapping.objects.filter(
            contest_id=contest_id
        ).values_list('question_id', flat=True)
        question_details = Question.objects.filter(
            id__in=contest_question_id_list
        ).values('id', 'type', 'description', 'question_text')
        for q in question_details:
            if q.get('type') == 'mcq':
                q['options'] = Answer.objects.filter(question_id=q.get('id')).first().expected_input.split(',')
        resp_dict = {
            "success": True,
            "questions_list": q
        }
        return Response(resp_dict, status=status.HTTP_200_OK)

    def get(self, request, **kwargs):
        pass


# class GetQuestionDetailsApi(APIView):
#     serializer_class = BeginContestSerializer

#     def post(self, request, **kwargs):
#         if not request.user.is_authenticated:
#             resp_dict = {
#                 "success": False,
#                 "error_message": "User not authenticated, Please Login."
#             }
#             return Response(resp_dict, status=status.HTTP_200_OK)
#         post_data = json.loads(request.data)
#         email = request.user.username
#         contest_id = post_data.get('contest_id', '')
#         if not contest_id:
#             resp_dict = {
#                 "success": False,
#                 "error_message": "Missing contest_id"
#             }
#             return Response(resp_dict, status=status.HTTP_200_OK)
#         user_contest_obj = UserContest.objects.filter(
#             contest_id=contest_id,
#             email=email,
#             user_start_time__isnull=True
#         )
#         if not user_contest_obj:
#             resp_dict = {
#                 "success": False,
#                 "error_message": "Unable to find any untaken contests."
#             }
#             return Response(resp_dict, status=status.HTTP_200_OK)
#         contest_question_id_list = ContestQuestionMapping.objects.filter(
#             contest_id=contest_id
#         ).values_list('question_id', flat=True)
#         question_details = Question.objects.filter(
#             id__in=contest_question_id_list
#         ).values('id', 'type', 'description', 'question_text')
#         for q in question_details:
#             if q.get('type') == 'mcq':
#                 q['options'] = Answer.objects.filter(question_id=q.get('id')).first().expected_input.split(',')
#         resp_dict = {
#             "success": True,
#             "questions_list": q
#         }
#         return Response(resp_dict, status=status.HTTP_200_OK)

#     def get(self, request, **kwargs):
#         pass
