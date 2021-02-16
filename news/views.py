from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
import crawling
import kakaotemplates
import tasks

@csrf_exempt
def callApi(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        print(data)
        client_utterance = data['userRequest']['utterance'].strip('\n')
        if client_utterance in crawling.carousel_keywords + crawling.basicCard_keywords:
            if tasks.REDIS.get(client_utterance):
                return JsonResponse(tasks.REDIS.get(client_utterance), status=200)
            return JsonResponse(kakaotemplates.keywords(client_utterance), status=200)
        elif client_utterance in ['보안', '안내', '키워드']:
            return JsonResponse(kakaotemplates.quickReplies(), status=200)
        else:
            if tasks.REDIS.get(client_utterance):
                return JsonResponse(tasks.REDIS.get(client_utterance), status=200)
            response = kakaotemplates.keywords(client_utterance)
            if response is False:
                return JsonResponse(kakaotemplates.simpleText(), status=200)
            tasks.REDIS.set(client_utterance, response)
            tasks.REDIS.expire(client_utterance, 600)
            return JsonResponse(response, status=200)