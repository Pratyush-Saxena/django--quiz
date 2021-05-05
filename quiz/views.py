from django.shortcuts import render,redirect
from .models import question
from django.core import serializers
import json
import random,html
from django.core.cache import cache
# Create your views here.

easy_quest=json.loads(serializers.serialize('json',question.objects.filter(level="Easy")))
hard_quest=json.loads(serializers.serialize('json',question.objects.filter(level="Hard")))
medium_quest=json.loads(serializers.serialize('json',question.objects.filter(level="Medium")))

def update_score(level):
    if level=="Easy":
        return 5
    elif level=="Medium":
        return 10
    else:
        return 15

def index(request):
    if request.method == "POST":
        return redirect('quiz/')
    return render(request,'quiz/p1.html')

def quiz(request):
    if request.method == "GET":
        request.session['count']=0
        request.session['score']=0
        request.session['level']="Easy"
        request.session['ques_list']=list()
        ques=easy_quest[random.randrange(0,len(easy_quest))]
    else:
        choice=eval(request.POST.get('choice'))
        request.session['curr_ques']['usr_ans']=choice
        request.session['ques_list'].append(request.session['curr_ques'])
        if request.session['count']==10:
            usr=dict()
            usr['ques_list']=request.session['ques_list']
            usr['score']=request.session['score']
            return render(request,'quiz/p3.html',{'usr_data':usr})
        if choice['Answer']:
            request.session['score']+=update_score(request.session['level'])
            if request.session['level']=="Easy":
                ques=medium_quest[random.randrange(0,len(medium_quest))]
                while(ques in request.session['ques_list']):
                    ques=medium_quest[random.randrange(0,len(medium_quest))]
                request.session['level']="Medium"
            else:
                ques=hard_quest[random.randrange(0,len(hard_quest))]
                while(ques in request.session['ques_list']):
                    ques=hard_quest[random.randrange(0,len(hard_quest))]
                request.session['level']="Hard"
        else:
            if request.session['level']=="Hard":
                ques=medium_quest[random.randrange(0,len(medium_quest))]
                while(ques in request.session['ques_list']):
                    ques=medium_quest[random.randrange(0,len(medium_quest))]
                request.session['level']="Medium"
            else:
                ques=easy_quest[random.randrange(0,len(easy_quest))]
                while(ques in request.session['ques_list']):
                    ques=medium_quest[random.randrange(0,len(medium_quest))]
                request.session['level']="Easy"
    request.session['curr_ques']=ques
    request.session['count']+=1
    return render(request,'quiz/p2.html',{"quest":ques,"count":request.session['count']})

def result(request):
    return render(request,'quiz/p3.html')


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