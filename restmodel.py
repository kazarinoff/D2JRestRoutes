from django.http import JsonResponse
import random, json, os
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.urls import path

from django.db import connection

def objectdict(x):
    od=x.__dict__
    od.pop('_state',None)
    return od

def RestfulModel(mmo):
    x=str(mmo._meta.model_name)
    y=mmo._meta.db_table
    class RestfulModelObject(mmo):
        def __init__(self):
            self.modelname=x
            self._table=y
        def _delete(self,eid):
            with connection.cursor() as cursor:
                cursor.execute(f"DELETE FROM {self._table} WHERE id = {eid}")
                return
        @csrf_exempt
        def create(self,request,post=False,csrf=False):
            @csrf_protect
            def postprotected(request):
                if (request.method=='POST'):
                    try:
                        params=request.POST.dict()
                        entry=mmo()
                        for key,value in params.items():
                            setattr(entry,key,value)
                        entry.save()
                        entry=mmo.objects.last()
                        return JsonResponse(objectdict(entry),safe=False)
                    except:
                        return JsonResponse({'msg':"Error. Couldn't create a "+self.modelname}, safe=False)
                else:
                    return JsonResponse({'msg':"Error. Couldn't create a "+self.modelname}, safe=False)
            
            def postunprotected(request):
                if (request.method=='POST'):
                    try:
                        params=request.POST.dict()
                        entry=mmo()
                        for key,value in params.items():
                            setattr(entry,key,value)
                        entry.save()
                        entry=mmo.objects.last()
                        return JsonResponse(objectdict(entry),safe=False)
                    except:
                        return JsonResponse({'msg':"Error. Couldn't create a "+self.modelname}, safe=False)
                else:
                    return JsonResponse({'msg':"Error. Couldn't create a "+self.modelname}, safe=False)
            if (post):
                if (csrf):
                    return postprotected(request)
                else:
                    return postunprotected(request)
            else:
                if (request.method=='POST'):
                    try:
                        params=request.POST.dict()
                        entry=mmo()
                        for key,value in params.items():
                            setattr(entry,key,value)
                        entry.save()
                        entry=mmo.objects.last()
                        return JsonResponse(objectdict(entry),safe=False)
                    except:
                        return JsonResponse({'msg':"Error. Couldn't create a "+self.modelname}, safe=False)
                else:
                    try:
                        params=request.GET.dict()
                        entry=mmo()
                        for key,value in params.items():
                            setattr(entry,key,value)
                        entry.save()
                        entry=mmo.objects.last()
                        return JsonResponse(objectdict(entry),safe=False)
                    except:
                        return JsonResponse({'msg':"Error. Couldn't create a "+self.modelname}, safe=False)

        @csrf_exempt
        def show(self,request,eid,post=False,csrf=False):
            if (post):
                if (request.method=='POST'):
                    if (csrf):
                        return edit(request,eid,csrf=True)
                    else:
                        return edit(request,eid,csrf=False)
            try:
                entry=mmo.objects.get(id=eid)
            except:
                return JsonResponse({'msg':"Error. Couldn't find a "+self.modelname+" with id "+str(eid)}, safe=False)
            return JsonResponse(objectdict(entry),safe=False)

        @csrf_exempt
        def edit(self,request,eid,post=False,csrf=False):
            try:
                entry=mmo.objects.get(id=eid)
            except:
                return JsonResponse({'msg':"Error. Couldn't find a "+self.modelname+" with id "+str(eid)}, safe=False)
            
            @csrf_protect
            def editprotected(request):
                if (request.method=='POST'):
                    params=request.POST.dict()
                    try:
                        for key,value in params.items():
                            setattr(entry,key,value)
                        entry=mmo.objects.get(id=eid)
                        entry.save()
                    except:
                        return JsonResponse({'msg':"Error. Couldn't edit "+self.modelname+" with id "+str(eid)}, safe=False)
                    return JsonResponse(objectdict(entry),safe=False)
                else:
                    return JsonResponse({'msg':"Error. Couldn't edit "+self.modelname+" with id "+str(eid)}, safe=False)
            
            def editunprotected(request):
                if (request.method=='POST'):
                    params=request.POST.dict()
                    try:
                        for key,value in params.items():
                            setattr(entry,key,value)
                        entry.save()
                        entry=mmo.objects.get(id=eid)
                    except:
                        return JsonResponse({'msg':"Error. Couldn't edit "+self.modelname+" with id "+str(eid)}, safe=False)
                    return JsonResponse(objectdict(entry),safe=False)
                else:
                    return JsonResponse({'msg':"Error. Couldn't edit "+self.modelname+" with id "+str(eid)}, safe=False)
            if (post):
                if (csrf):
                    return editprotected(request)
                else:
                    return editunprotected(request)
            else:
                if request.method=='POST':
                    params=request.POST.dict()
                    try:
                        for key,value in params.items():
                            setattr(entry,key,value)
                        entry.save()
                        entry=mmo.objects.get(id=eid)
                    except:
                        return JsonResponse({'msg':"Error. Couldn't edit "+self.modelname+" with id "+str(eid)}, safe=False)
                    return JsonResponse(objectdict(entry),safe=False)
                elif request.method=='GET':
                    params=request.GET.dict()
                    try:
                        for key,value in params.items():
                            setattr(entry,key,value)
                        entry.save()
                        entry=mmo.objects.get(id=eid)
                    except:
                        return JsonResponse({'msg':"Error. Couldn't edit "+self.modelname+" with id "+str(eid)}, safe=False)
                    return JsonResponse(objectdict(entry),safe=False)
                else:
                    return JsonResponse({'msg':"Error. Couldn't edit "+self.modelname+" with id "+str(eid)}, safe=False)

        def index(self,request):
            entrys=mmo.objects.all()
            entryarray=[]
            for entry in entrys:
                entryarray.append(objectdict(entry))
            return JsonResponse({self.modelname+"s":entryarray},safe=False)
        
        @csrf_exempt
        def delete(self,request,eid,post=False,csrf=False):
            if (post):
                if request.method=='POST':
                    try:
                        entry=mmo.objects.get(id=eid)
                    except:
                        return JsonResponse({'msg':"Error. Couldn't find "+self.modelname+" with id "+str(eid)}, safe=False)
                    try:
                        self._delete(eid)
                        return JsonResponse({'msg':self.modelname+" with id "+str(eid)+" deleted"}, safe=False)
                    except:
                        return JsonResponse({'msg':"Error. Couldn't delete "+self.modelname+" with id "+str(eid)}, safe=False)
                else:
                    return JsonResponse({'msg':"Error. Couldn't edit "+self.modelname+" with id "+str(eid)}, safe=False)
            else:
                try:
                    entry=mmo.objects.get(id=eid)
                except:
                    return JsonResponse({'msg':"Error. Couldn't find "+self.modelname+" with id "+str(eid)}, safe=False)
                try:
                    self._delete(eid)
                    return JsonResponse({'msg':self.modelname+" with id "+str(eid)+" deleted"}, safe=False)
                except:
                    return JsonResponse({'msg':"Error. Couldn't delete "+self.modelname+" with id "+str(eid)}, safe=False) 

        def search(self,request):
            if (request.method=='GET'):
                params=request.GET.dict()
            elif (request.method=='POST'):
                params=request.POST.dict()
            else:
                params=request.GET.dict().items()
            entrys=mmo.objects.filter(**params)
            entryarray=[]
            for entry in entrys:
                entryarray.append(objectdict(entry))
            return JsonResponse({self.modelname+"s":entryarray},safe=False)

        def random(self,request):
            try:
                x=mmo.objects.last().id
            except:
                return JsonResponse({'msg':"Error. Random is broken"}, safe=False)
            counter=1
            while (counter<50):
                entryid=random.randint(1,x)
                try:
                    entry=mmo.objects.get(id=entryid)
                    return JsonResponse(objectdict(entry),safe=False)
                except:
                    counter+=1
            return JsonResponse({'msg':"Error. Random is broken. You may have deleted too many database entries"}, safe=False)

        def default_routes(self,post=False,csrf=False):
            url_patterns=[
                path('all/',self.index,name='all'),
                path('index/',self.index,name='index'),
                path('create/',self.create,{'post':post,'csrf':csrf},name='create'),
                path('new/',self.create,{'post':post,'csrf':csrf},name='new'),
                path('<int:eid>/',self.show,{'post':post,'csrf':csrf},name='show'),
                path('<int:eid>/delete/',self.delete,{'post':post,'csrf':csrf},name='delete'),
                path('<int:eid>/edit/',self.edit,{'post':post,'csrf':csrf},name='edit'),
                path('search/',self.search,name='search'),   
                path('random/',self.random,name='random'),         
            ]
            return url_patterns
        def index_route(self,url='index'):
            return [path(url+"/",self.index,name='all')]
        def show_route(self,post=False,csrf=False):
            return [path('<int:eid>/',self.show,{'post':post,'csrf':csrf},name='show')]
        def create_route(self,url='create',post=False,csrf=False):
            return [path(url+'/',self.create,{'post':post,'csrf':csrf},name='create')]
        def edit_route(self,url='edit',post=False,csrf=False):
            return [path('<int:eid>/'+url+'/',self.edit,{'post':post,'csrf':csrf},name='edit')]
        def delete_route(self,url='delete',post=False,csrf=False):
            return [path('<int:eid>/'+url+'/',self.delete,{'post':post,'csrf':csrf},name='delete')]
        def search_route(self,url='search'):
            return [path(url+"/",self.search,name='search')]
        def random_route(self,url='random'):
            return [path(url+"/",self.random,name='random')]


    return RestfulModelObject()