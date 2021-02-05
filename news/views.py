from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
import crawling
import kakaotemplates

@csrf_exempt
def callApi(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        print(data)
        client_utterance = data['userRequest']['utterance'].strip('\n')

        if client_utterance in crawling.carousel_keywords + crawling.basicCard_keywords:
            return JsonResponse(kakaotemplates.keywords(client_utterance), status=200)
        else:
            response = kakaotemplates.keywords(client_utterance)
            if response is False:
                return JsonResponse(kakaotemplates.quickReplies(), status=200)
            return JsonResponse(response, status=200)