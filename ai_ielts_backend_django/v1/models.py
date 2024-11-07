from __future__ import annotations
from django.db import models
from django.contrib.auth.models import AbstractUser
import json

# Create your models here.
class QuestionGroup(models.Model):
    QUESTION_GROUP_TYPES = [
        ("1", "Part 1"),
        ("2&3", "Part 2 & 3")
    ]
    id = models.AutoField("question group id", primary_key=True)
    name = models.CharField("question group name", max_length=100)
    type = models.CharField("question group type (1 or 2&3)", max_length=10, choices=QUESTION_GROUP_TYPES)
    topic = models.CharField("question group topic", max_length=200)
    description = models.TextField("question group description")
    createTime = models.DateTimeField("question group created time", auto_now_add=True)
    modifiedTime = models.DateTimeField("question group modified time", auto_now=True)
    
    def toObject(self):
        questions = Question.objects.filter(questionGroup=self).all()
        return {
            "id": self.id,
            "name": self.name,
            "topic": self.topic,
            "description": self.description,
            "type": self.type,
            "questions": [question.toObject() for question in questions]
        }
        
    def __str__(self):
        return self.name
    
    

class User(AbstractUser):
    id = models.AutoField("user id", primary_key=True)
    username = models.CharField("user name", max_length=200, unique=True)
    token = models.CharField("user token", max_length=100)
    questionGroupLearningProgress = models.ManyToManyField(
        QuestionGroup, 
        through="LearningProgress",
        through_fields=("user", "questionGroup"),
        verbose_name="user learning progress for some question group"
    )
    createTime = models.DateTimeField("user created time", auto_now_add=True)
    modifiedTime = models.DateTimeField("user modified time", auto_now=True)
    
    
class LearningProgress(models.Model):
    # id = models.AutoField("learning progress id", primary_key=True)
    questionGroup = models.ForeignKey(QuestionGroup, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    isCompleted = models.BooleanField("Has this question group already learnt?")
    createTime = models.DateTimeField("learning progress created time", auto_now_add=True)
    modifiedTime = models.DateTimeField("learning progress modified time", auto_now=True)
    
    # class Meta:
    #     unique_together = ['questionGroup', 'user']
    

class Question(models.Model):
    PART_TYPES = [
        (1, "Part 1"),
        (2, "Part 2"),
        (3, "Part 3")
    ]
    id = models.AutoField("question id", primary_key=True)
    questionGroup = models.ForeignKey(QuestionGroup, on_delete=models.CASCADE, verbose_name="question group id for question")
    partType = models.BigIntegerField("part type (1 or 2 or 3)", choices=PART_TYPES)
    content = models.TextField("question content")
    createTime = models.DateTimeField("question created time", auto_now_add=True)
    modifiedTime = models.DateTimeField("question modified time", auto_now=True)
    
    def toObject(self):
        return {
            "id": self.id,
            "part": self.partType,
            "content": self.content
        }
        
    def __str__(self):
        return self.content
    

class Session(models.Model):
    id = models.AutoField("session id", primary_key=True)
    questionGroups = models.ManyToManyField(QuestionGroup, verbose_name="question groups")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="user id related to session")
    openaiSessionId = models.CharField("openai session id", max_length=100)
    createTime = models.DateTimeField("session created time", auto_now_add=True)
    modifiedTime = models.DateTimeField("session modified time", auto_now=True)
    
    def set(self, userId: str | None, openaiSessionId: str | None):
        if userId is not None:
            self.user = User.objects.filter(id=userId).first()
        if openaiSessionId is not None:
            self.openaiSessionId = openaiSessionId
        print(self.id)
        self.save()
        print(self.id)
        
    def retrieveQuestions(self):
        groupsForPart1 = QuestionGroup.objects.filter(type="1").order_by("?").all()[:10]
        groupsForPart23 = QuestionGroup.objects.filter(type="2&3").order_by("?").all()[:10]
        self.questionGroups.set(groupsForPart1 | groupsForPart23)
        print(self.questionGroups)
        
    def questionGroupsToCSV(self):
        fieldsTemplate = "\"{}\",\"{}\",\"{}\",\"{}\"\n"
        csvOutput = fieldsTemplate.format("part", "question", "topic", "question_group_id")
        for questionGroup in self.questionGroups.all():
            questions = Question.objects.filter(questionGroup=questionGroup).all()
            for question in questions:
                line = fieldsTemplate.format(
                    question.partType,
                    question.content,
                    questionGroup.topic,
                    questionGroup.id
                )
                # line = re.escape(line)
                csvOutput += line
        return csvOutput
        
    def toObject(self):
        return {
            "id": self.id,
            "user_id": self.user.id,
            "openai_session_id": self.openaiSessionId,
            "question_groups": [
                questionGroup.toObject() for questionGroup in list(self.questionGroups.all())
            ],
            "questions_csv": self.questionGroupsToCSV()
        }
        
    def __str__(self):
        return "{}_{}_{}".format(self.id, self.openaiSessionId, self.user.username)
    
    
    