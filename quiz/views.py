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

cache.set('name',"xyz",None)
cache.set('score',0,None)
cache.set('level',"Easy",None)
cache.set('ques_count',0,None)
def index(request):
    if request.method == "POST":
        cache.set('name',request.POST.get('name'),None)
        cache.set('score',0,None)
        cache.set('level',"Easy",None)
        cache.set('ques_count',0,None)
        return redirect('quiz/')
    return render(request,'quiz/p1.html')

def quiz(request):
    if request.method == "GET":
        ques=easy_quest[random.randrange(0,len(easy_quest))]
    else:
        choice=eval(request.POST.get('choice'))
        if choice['Answer']:
            if cache.get('level')=="Easy":
                ques=medium_quest[random.randrange(0,len(medium_quest))]
                cache.set('level',"Medium",None)
            else:
                ques=hard_quest[random.randrange(0,len(hard_quest))]
                cache.set('level',"Hard",None)
        else:
            if cache.get('level')=="Hard":
                ques=medium_quest[random.randrange(0,len(medium_quest))]
                cache.set('level',"Medium",None)
            else:
                ques=easy_quest[random.randrange(0,len(easy_quest))]
                cache.set('level',"Easy",None)
    cache.incr('ques_count')
    count=cache.get('ques_count')
    return render(request,'quiz/p2.html',{"quest":ques,"count":count})

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