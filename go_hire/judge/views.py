from django.shortcuts import render
import json
from judge.constants import supported_language, supported_languages
from judge.config import  ideone_config
import requests
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from judge.models import UserSubMissionTable
from question.models import Answer
# Create your views here.

@csrf_exempt
def compile(request):
    '''
      Method : Post
      Content-Type: application/json
      Body
    # type
    # source_code
    # language
    # ques_id
    # contest_id
    # user_id
    # time_limit(optional)
    # custom_input(optional)
    '''
    resp = {
        'status':'failed',
        'body': "this will be the response"
    }
    if request.method == 'POST':
        data = json.loads(request.body)
        source_code = data.get('source_code','')
        language = data.get('language', '')
        ques_id = data.get('ques_id', '')
        contest_id = data.get('contest_id', '')
        user_id = str(request.user.id)
        time_limit = data.get('time_limit', '')
        custom_input = data.get('custom_input', '')
        type = data.get('type','')
        input = ''
        input_from_db = Answer.objects.filter(question_id=ques_id).first()
        if  input_from_db :
            input = input_from_db.expected_input
        if not validate_compile_data(source_code, ques_id, contest_id, language, user_id):
            return resp
        else:
            if custom_input != '':
                input = custom_input
            if type == 'compile':
                input = ''
            api = "compile"
            api_type = "prod"
            ideone_url = ideone_config[api_type]["protocol"]+ideone_config[api_type]["host"]+ideone_config[api_type]["endpoint"][api]
            body = {
                "compilerId": supported_languages[language],
                "source": source_code,
                "input": input
            }
            params = {
                'access_token': ideone_config[api_type]['access-token']
            }

            headers = {
                'content-type':'application/json'
            }
            ideone_resp = requests.post(ideone_url, data = json.dumps(body), headers = headers, params=params)
            if ideone_resp.status_code in (200, 201):
                ideone_resp = ideone_resp.json()
                resp = {
                    'status':'success',
                    'message':'successfully compiled'
                }
                if type != 'compile':
                    resp['message'] = 'successfully submitted'
                    resp['id'] = ideone_resp['id']
                    save_user_submission(data, ideone_resp.get("id", ''))
            return JsonResponse(resp)
    return JsonResponse(resp)

def validate_compile_data(source_code, ques_id, contest_id, language, user_id):
    if source_code == '' or ques_id == '' or contest_id == '' or user_id == '':
        return False
    return True

def get_submission_result(request):
    # get_params : id, ques_id

    submission_id = request.GET.dict().get('id','')
    ques_id = request.GET.dict().get('ques_id','')
    resp = {
        'status': 'failed'
    }
    if submission_id is None:
        return  JsonResponse(resp)
    else:
        api = 'submission_result'
        api_type = 'prod'
        ideone_url = ideone_config[api_type]["protocol"] + ideone_config[api_type]["host"] + \
                     ideone_config[api_type]["endpoint"][api]+submission_id
        params = {
            'access_token': ideone_config[api_type]['access-token']
        }
        ideone_resp = requests.get(ideone_url, params= params)
        if ideone_resp.status_code not in (200, 201):
            return JsonResponse(resp)
        else:
            ideone_resp = ideone_resp.json()
            result = ideone_resp.get('result')
            resp['compile_info_name'] = result.get('status').get("name")
            compile_code = result.get('status').get("code")
            if compile_code in (11,12):
                compile_info_uri = result.get("streams", {}).get("cmpinfo",{}).get("uri",'')
                compile_info_resp = requests.get(compile_info_uri)
                if compile_info_resp.status_code in (200, 201):
                    compile_info_resp = str(compile_info_resp.content)
                    resp['output_info_resp'] = compile_info_resp
                    update_user_submission(submission_id, '', compile_info_resp)
            elif compile_code == 15:
                output_info_uri = result.get("streams", {}).get("output", {}).get("uri", '')
                output_info_resp = requests.get(output_info_uri)
                if output_info_resp.status_code in (200, 201):
                    output_info_resp = str(output_info_resp.content)
                    output_from_file = Answer.objects.filter(question_id = ques_id)
                    if output_from_file and str(output_from_file[0].expected_output) == output_info_resp:
                        resp['output_info_resp'] = output_info_resp
                        update_user_submission(submission_id, '', output_info_resp)
            else:
                update_user_submission(submission_id, 'success', '')
                resp['status'] = 'success'
        return JsonResponse(resp)


def save_user_submission(data, id):
    obj = UserSubMissionTable(
        user_id = data.get('user_id',''),
        source_code = data.get('source_code', ''),
        ques_id =  data.get('ques_id', ''),
        submission_id = id,
        contest_id  = data.get('contest_id', ''),
    )
    obj.save()

def update_user_submission(submission_id, result, response):
    obj = UserSubMissionTable.object.filter(submission_id)
    obj.result = result
    obj.response = response
    obj.save()




