from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.core.files.storage import FileSystemStorage
import json
from .models import Session

@csrf_exempt
def sessionAPI(request: HttpRequest):
    # csrf_token = request.META['CSRF_COOKIE'] 
    if request.method == "POST":
        data = json.loads(request.body)
        userId = int(data["user_id"])
        openaiSessionId = data["openai_session_id"]
        session = Session(userId, openaiSessionId)
        session.save()
        responseData = {
            "status": "successful",
            "result": session.toObject()
        }
        return JsonResponse(responseData)
    return JsonResponse({"status": "unsupport method"})


@csrf_exempt
def upload_file(request):
    if request.method == 'POST' and request.FILES['file']:
        # Get the uploaded file from the request
        uploaded_file = request.FILES['file']
        
        # Save the file
        fs = FileSystemStorage()
        filename = fs.save(uploaded_file.name, uploaded_file)
        uploaded_file_url = fs.url(filename)
        
        return HttpResponse(f"File uploaded successfully: {uploaded_file_url}")
    return render(request, 'upload.html')