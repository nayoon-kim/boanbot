from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from main import Messages

@csrf_exempt
def callApi(request):
    messages = Messages()
    if request.method == 'POST':
        data = JSONParser().parse(request)
        client_utterance = data['userRequest']['utterance'].strip('\n')

        return JsonResponse(messages.reply(client_utterance), status=200)