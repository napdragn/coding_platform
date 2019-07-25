from django.shortcuts import render
import json
from judge.constants import supported_language, supported_languages
from judge.config import  ideone_config
import requests
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
# Create your views here.

@csrf_exempt
def compile(request):
    '''
      Method : Post
      Content-Type: application/json
      Body

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
        user_id = data.get('user_id','')
        time_limit = data.get('time_limit', '')
        custom_input = data.get('custom_input', '')
        if not valid_compile_data(source_code, ques_id, contest_id, language, user_id):
            return resp
        if custom_input == '':
            return resp
        else:
            api = "compile"
            api_type = "prod"
            ideone_url = ideone_config[api_type]["protocol"]+ideone_config[api_type]["host"]+ideone_config[api_type]["endpoint"][api]
            body = {
                "compilerId": supported_languages[language],
                "source": source_code,
                "input": custom_input
            }
            params = {
                'access_token': ideone_config[api_type]['access-token']
            }

            headers = {
                'content-type':'application/json'
            }
            import pdb;
            pdb.set_trace()
            ideone_resp = requests.post(ideone_url, data = json.dumps(body), headers = headers, params=params)
            if ideone_resp.status_code in (200, 201):
                ideone_resp = ideone_resp.json()
                resp = {
                    'status':'success',
                    'body':ideone_resp
                }
            return JsonResponse(resp)
            #save id of the submitted code in the db against the user_id, question_id,contest_id

    return JsonResponse(resp)

def valid_compile_data(source_code, ques_id, contest_id, language, user_id):
    if source_code == '' or ques_id == '' or contest_id == '' or user_id == '':
        return False
    return True
