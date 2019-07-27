from django.shortcuts import render
from django.http import JsonResponse
import yagmail
# Create your views here.


def send_email(request):
    yag = yagmail.SMTP('bishukumar017@gmail.com', '13613469')
    yag.send('deepakgupta007007@gmail.com', 'Test Mail for GoHire!', ['Yo this is the body!', '#GoBefikar'])
    return JsonResponse({"status":"success"})