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

usr={'name':'xyz'}
ques=dict()
ques_count=0
level="Easy"



def index(request):
    global usr
    if request.method == "POST":
        usr['name']=request.POST.get('name')
        usr['score']=0
        usr['ques_list']=list()
        level="Easy"
        ques_count=1
        return redirect('quiz/')
    return render(request,'quiz/p1.html')

def quiz(request):
    global usr,ques,ques_count,level
    if request.method == "GET":
        ques=easy_quest[random.randrange(0,len(easy_quest))]
    else:
        choice=eval(request.POST.get('choice'))
        if choice['Answer']:
            if level=="Easy":
                ques=medium_quest[random.randrange(0,len(medium_quest))]
                level="Medium"
            else:
                ques=hard_quest[random.randrange(0,len(hard_quest))]
                level="Hard"
        else:
            if level=="Hard":
                ques=medium_quest[random.randrange(0,len(medium_quest))]
                level="Medium"
            else:
                ques=easy_quest[random.randrange(0,len(easy_quest))]
                level="Easy"
    ques_count+=1
    return render(request,'quiz/p2.html',{"quest":ques,"count":ques_count})
    

def result(request):
    global usr
    return render(request,'quiz/p3.html',{'usr_data':usr})


"""global ques_count,ques
    if request.method == "GET":
        ques_count=1
        usr['score']=0
        usr['easy_count']=0
        usr['medium_count']=0
        usr['hard_count']=0
        usr['ques_list']=list()
        ques=easy_quest[random.randrange(0,len(easy_quest))]
    elif request.method == "POST":
        for a in ques['fields']['answer']:
            if a['Value']==dict(request.POST.get('choice'))['Value']:
                q=ques
                q.update({'usr_ans':a})
                usr['ques_list'].append(q)
                if a['Answer']:
                    usr['score']+=ques['fields']['score']
                    if ques['fields']['level']=="Easy":
                        usr['easy_count']+=1
                        ques=medium_quest[random.randrange(0,len(medium_quest))]
                    else:
                        if ques['fields']['level']=="Hard":
                            usr['hard_count']+=1
                        else:
                            usr['medium_count']+=1
                        ques=hard_quest[random.randrange(0,len(hard_quest))]
                else:
                    if ques['fields']['level']=="Hard":
                        ques=medium_quest[random.randrange(0,len(medium_quest))]
                    else:
                        ques=easy_quest[random.randrange(0,len(easy_quest))]
        ques_count+=1
        print(request.POST.get('choice'))"""