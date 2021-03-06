import datetime
import json

from django.utils import timezone

from contests.models import Contest, ContestQuestionMapping, UserContest
from contests.serializer import BeginContestSerializer, GetContestsSerializer, SubmitContestSerializer
from question.models import Answer, Question, QuestionTagMapping, Tag
from judge.models import UserSubMissionTable
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from django.contrib.auth.models import User

class GetContestsApi(APIView):
    serializer_class = GetContestsSerializer

    def post(self, request, **kwargs):
        pass

    def get(self, request, **kwargs):
        user_id = request.GET.get('user_id')
        userx = User.objects.get(id=user_id)
        # if not userx.is_authenticated:
        #     resp_dict = {
        #         "success": False,
        #         "error_message": "User not authenticated, Please Login."
        #     }
        #     return Response(resp_dict, status=status.HTTP_200_OK)
        email = userx.username
        user_contest_list = UserContest.objects.filter(
            email=email,
            user_end_time__isnull=True
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
        # if not request.user.is_authenticated:
        #     resp_dict = {
        #         "success": False,
        #         "error_message": "User not authenticated, Please Login."
        #     }
        #     return Response(resp_dict, status=status.HTTP_200_OK)

        post_data = request.data
        user_id = post_data.get('user_id')
        userx = User.objects.get(id=user_id)
        email = userx.username
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
            user_end_time__isnull=True
        ).first()
        if not user_contest_obj:
            resp_dict = {
                "success": False,
                "error_message": "Unable to find any untaken contests."
            }
            return Response(resp_dict, status=status.HTTP_200_OK)
        user_contest_obj.user_start_time = datetime.datetime.now()
        user_contest_obj.save()
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
            "questions_list": question_details
        }
        return Response(resp_dict, status=status.HTTP_200_OK)

    def get(self, request, **kwargs):
        pass


class GetQuestionDetailsApi(APIView):
    serializer_class = BeginContestSerializer

    def post(self, request, **kwargs):
        pass

    def get(self, request, **kwargs):
        get_data = request.GET.dict()
        user_id = get_data.get('user_id')
        userx = User.objects.get(id=user_id)
        email = userx.username
        question_id = get_data.get('question_id', '')
        contest_id = get_data.get('contest_id', '')
        if not question_id:
            resp_dict = {
                "success": False,
                "error_message": "Missing question_id"
            }
            return Response(resp_dict, status=status.HTTP_200_OK)
        user_contest_obj = UserContest.objects.filter(
            contest_id=contest_id,
            email=email,
            user_end_time__isnull=True
        )
        if not user_contest_obj:
            resp_dict = {
                "success": False,
                "error_message": "Not authorized to view this question."
            }
            return Response(resp_dict, status=status.HTTP_200_OK)
        contest_question_id_list = ContestQuestionMapping.objects.filter(
            contest_id=contest_id
        ).values_list('question_id', flat=True)
        # if question_id not in contest_question_id_list:
        #     resp_dict = {
        #         "success": False,
        #         "error_message": "Not authorized to view this question."
        #     }
        #     return Response(resp_dict, status=status.HTTP_200_OK)

        question_obj = Question.objects.filter(
            id=question_id
        )
        if not question_obj:
            resp_dict = {
                "success": False,
                "error_message": "Invalid Question Id given."
            }
        else:
            question_details = question_obj.values('description', 'question_text')
            resp_dict = {
                "success": True,
                "question_details": question_details
            }
        return Response(resp_dict, status=status.HTTP_200_OK)
        

class SubmitContestApi(APIView):
    serializer_class = SubmitContestSerializer

    def get(self, request, **kwargs):
        pass

    def post(self, request, **kwargs):
        # if not request.user.is_authenticated:
        #     resp_dict = {
        #         "success": False,
        #         "error_message": "User not authenticated, Please Login."
        #     }
        #     return Response(resp_dict, status=status.HTTP_200_OK)
        post_data = request.data
        user_id = post_data.get('user_id')
        userx = User.objects.get(id=user_id)
        answers_list = post_data.get('answer_list')
        contest_id = post_data.get('contest_id')
        for answer_list in answers_list:
            ans = Answer.objects.filter(question_id=answer_list.get('question_id')).first().expected_output
            result = '100' if ans == answer_list.get('answer') else '0'
            UserSubMissionTable.objects.create(
                user_id=userx.id,
                contest_id=contest_id,
                ques_id=answer_list.get('question_id'),
                source_code='',
                result=result,
                response=answer_list.get('answer'),
            )
        UserContest.objects.filter(
            email=userx.email,
            contest_id=contest_id,
        ).update(user_end_time=timezone.now())

        resp_dict = {
            "success": True,
            "message": "Contest successfully done."
        }
        return Response(resp_dict, status=status.HTTP_200_OK)
