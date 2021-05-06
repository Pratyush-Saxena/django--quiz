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
    return render(request,'quiz/index.html')

def quiz(request):
    if request.method == "GET":
        request.session['count']=0
        request.session['score']=0
        request.session['level']="Easy"
        request.session['ques_list']=list()
        request.session['easy_ques_itr']=0
        request.session['med_ques_itr']=0
        request.session['hard_ques_itr']=0
        ques=easy_quest[request.session['easy_ques_itr']]
        request.session['easy_ques_itr']+=1
    else:
        choice=eval(request.POST.get('choice'))
        request.session['curr_ques']['usr_ans']=choice
        request.session['ques_list'].append(request.session['curr_ques'])
        if request.session['count']==10:
            usr=dict()
            usr['ques_list']=request.session['ques_list']
            usr['score']=request.session['score']
            return render(request,'quiz/result.html',{'usr_data':usr})
        if choice['Answer']:
            request.session['score']+=update_score(request.session['level'])
            if request.session['level']=="Easy":
                ques=medium_quest[request.session['med_ques_itr']]
                request.session['med_ques_itr']+=1
                request.session['level']="Medium"
            else:
                ques=hard_quest[request.session['hard_ques_itr']]
                request.session['hard_ques_itr']+=1
                request.session['level']="Hard"
        else:
            if request.session['level']=="Hard":
                ques=medium_quest[request.session['med_ques_itr']]
                request.session['med_ques_itr']+=1
                request.session['level']="Medium"
            else:
                ques=easy_quest[request.session['easy_ques_itr']]
                request.session['easy_ques_itr']+=1
                request.session['level']="Easy"
    request.session['curr_ques']=ques
    request.session['count']+=1
    return render(request,'quiz/quiz.html',{"quest":ques,"count":request.session['count']})



