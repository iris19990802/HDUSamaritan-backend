from django.http import HttpResponse,JsonResponse
from django.views.decorators.csrf import csrf_exempt
 

# @csrf_exempt
# def login(request):
#     #return HttpResponse("Hello world ! ")
#     return JsonResponse({'value':1})