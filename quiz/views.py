from django.shortcuts import render,redirect
from .models import question
from django.core import serializers
import json
import random,html
# Create your views here.
htmlCodes = (
            ("'", "&#039;"),
            ('"', '&quot;'),
            ('>', '&gt;'),
            ('<', '&lt;'),
            ('&', '&amp;'),
            
        )
easy_quest=json.loads(serializers.serialize('json',question.objects.filter(level="Easy")))
hard_quest=json.loads(serializers.serialize('json',question.objects.filter(level="Hard")))
medium_quest=json.loads(serializers.serialize('json',question.objects.filter(level="Medium")))

def index(request):
    if request.method == "POST":
        global usr
        usr=dict()
        usr['name']=request.POST.get('name')
        return redirect('quiz/')
    return render(request,'quiz/p1.html')
def quiz(request):
    if request.method == "GET":
        global ques,ques_count
        ques_count=1
        usr['score']=0
        usr['easy_count']=0
        usr['medium_count']=0
        usr['hard_count']=0
        usr['ques_list']=list()
        ques=easy_quest[random.randrange(0,len(easy_quest))]
    elif request.method == "POST":
        for a in ques['fields']['answer']:
            if a['Value']==request.POST.get('choice'):
                q=ques
                q.update({'usr_ans':a})
                usr['ques_list'].append(q)
                if a['Answer']:
                    usr['score']+=ques['fields']['score']
                    if ques['fields']['level']=="Easy":
                        usr['easy_count']+=1
                        while(ques in usr['ques_list']):
                            ques=medium_quest[random.randrange(0,len(medium_quest))]
                    else:
                        if ques['fields']['level']=="Hard":
                            usr['hard_count']+=1
                        else:
                            usr['medium_count']+=1
                        while(ques in usr['ques_list']):
                            ques=hard_quest[random.randrange(0,len(hard_quest))]
                else:
                    if ques['fields']['level']=="Hard":
                        while(ques in usr['ques_list']):
                            ques=medium_quest[random.randrange(0,len(medium_quest))]
                    else:
                        while(ques in usr['ques_list']):
                            ques=easy_quest[random.randrange(0,len(easy_quest))]
        ques_count+=1
        ques['fields']['question']=html.unescape(ques['fields']['question'])
        for code in htmlCodes:
            ques['fields']['question']=ques['fields']['question'].replace(code[1],code[0])
        for a in ques['fields']['answer']:
            a['value']=html.unescape(a['Value'])
            for code in htmlCodes:
                a['Value']=a['Value'].replace(code[1],code[0])
    return render(request,'quiz/p2.html',{"quest":ques,"count":ques_count})

def result(request):
    return render(request,'quiz/p3.html',{'usr_data':usr})