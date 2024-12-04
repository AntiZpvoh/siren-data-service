from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage
import json
from .models import Session, QuestionGroup, Question

@csrf_exempt
def createSession(request: HttpRequest):
    if request.method == "POST":
        data = json.loads(request.body)
        userId = int(data["user_id"]) if "user_id" in data else None
        openaiSessionId = data["openai_session_id"] if "openai_session_id" in data else None
        session = Session()
        session.set(userId, openaiSessionId)
        session.retrieveQuestions()
        session.save()
        responseData = {
            "status": "successful",
            "result": session.toObject()
        }
        return JsonResponse(responseData)
        
    return JsonResponse({"status": "unsupport method"})


@csrf_exempt
def getOrPutSession(request: HttpRequest, sessionId):
    if request.method == "GET":
        session = Session.objects.filter(id=sessionId).first()
        print(session)
        responseData = session.toObject()
        return JsonResponse(responseData)
    elif request.method == "PUT":
        session = Session.objects.filter(id=sessionId).first()
        print(session)
        data = json.loads(request.body)
        userId = int(data["user_id"]) if "user_id" in data else None
        openaiSessionId = data["openai_session_id"] if "openai_session_id" in data else None
        session.set(userId, openaiSessionId)
        session.save()
        responseData = session.toObject()
        return JsonResponse(responseData)
        
    return JsonResponse({"status": "unsupport method"})


@csrf_exempt
def getSessionQuestionsCSV(request: HttpRequest, sessionId):
    if request.method == "GET":
        session = Session.objects.filter(id=sessionId).first()
        print(session)
        responseData = {
            "status": "successful",
            "result": session.questionGroupsToCSV()
        }
        return JsonResponse(responseData)
        
    return JsonResponse({"status": "unsupport method"})


@csrf_exempt
def updateSession(request: HttpRequest, sessionId):
    if request.method == "PUT":
        session = Session.objects.filter(id=sessionId).first()
        print(session)
        data = json.loads(request.body)
        userId = int(data["user_id"]) if "user_id" in data else None
        openaiSessionId = data["openai_session_id"] if "openai_session_id" in data else None
        session.set(userId, openaiSessionId)
        session.save()
        responseData = session.toObject()
        return JsonResponse(responseData)
        
    return JsonResponse({"status": "unsupport method"})


@csrf_exempt
def createQuestion(request: HttpRequest, questionGroupId):
    if request.method == "POST":
        data = json.loads(request.body)
        partType = int(data["partType"]) if "partType" in data else None
        content = data["content"] if "content" in data else None
        questionGroup = QuestionGroup.objects.filter(id=questionGroupId).first()
        
        question = Question()
        question.partType = partType
        question.content = content
        question.questionGroup = questionGroup
        question.save()
        responseData = {
            "status": "successful",
            "result": question.toObject()
        }
        return JsonResponse(responseData)
        
    return JsonResponse({"status": "unsupport method"})


@csrf_exempt
def createQuestionGroup(request: HttpRequest):
    if request.method == "POST":
        data = json.loads(request.body)
        name = data["name"] if "name" in data else None
        type = data["type"] if "type" in data else None
        topic = data["topic"] if "topic" in data else None
        description = data["description"] if "description" in data else None
        questionGroup = QuestionGroup()
        questionGroup.name = name
        questionGroup.type = type
        questionGroup.topic = topic
        questionGroup.description = description
        questionGroup.save()
        responseData = {
            "status": "successful",
            "result": questionGroup.toObject()
        }
        return JsonResponse(responseData)
        
    return JsonResponse({"status": "unsupport method"})