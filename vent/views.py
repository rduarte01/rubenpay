from django.shortcuts import render
 
# Instanciamos las vistas genéricas de Django 
from django.views.generic import ListView, DetailView 
from django.views.generic.edit import CreateView, UpdateView, DeleteView

# Nos sirve para redireccionar despues de una acción revertiendo patrones de expresiones regulares 
from django.urls import reverse
 
# Habilitamos el uso de mensajes en Django
from django.contrib import messages 
 
# Habilitamos los mensajes para class-based views 
from django.contrib.messages.views import SuccessMessageMixin 
 
# Habilitamos los formularios en Django
from django import forms
from django.contrib.auth.decorators import login_required,permission_required
from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib import messages
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from vent.api import *

###########################################
LISTA_CAMBIOS = dict()
###########################################

@login_required(login_url='/login/')
def deuda_list(request):

    list = api_deuda_list()

    template_name = 'deuda_list.html'

    context={
        'obj':list,
    }
    return render(request,template_name,context)

@login_required(login_url='/login/')
def deuda_new(request):
    template = 'deuda_form.html'
    fecha_actual = timezone.now().date()

    if request.method == "POST":

        idDeuda  = request.POST.get("docId")
        label  = request.POST.get("label")
        value  = request.POST.get("value")
        start  = request.POST.get("start")
        end  = request.POST.get("end")
        start_time  = request.POST.get("start-time")
        end_time  = request.POST.get("end-time")
        f1 = str(start) +"T"+str(start_time) +":00"
        f2 = str(end) +"T"+str(end_time) +":00"
        #print(docId)
        print(label)
        print(value)
        print(f1)
        print(f2)
        api_deuda_new(idDeuda,f1,f2,value,label)

        return redirect('vent:deuda_list')


    context={
        'obj':None,
        'fecha_actual':fecha_actual,
    }
    return render(request,template,context)

@login_required(login_url='/login/')
def deuda_edit(request,idDoc):
    template = 'deuda_form.html'
    fecha_actual = timezone.now().date()
    obj = dict()
    print("-------------------------------------------------")
    docId,label,payUrl,value,start,end,status = api_deuda(idDoc)
    print("-------------------------------------------------")

    if request.method == "POST":

        idDeuda  = request.POST.get("docId")
        label  = request.POST.get("label")
        value  = request.POST.get("value")
        start  = request.POST.get("start")
        end  = request.POST.get("end")
        start_time  = request.POST.get("start-time")
        end_time  = request.POST.get("end-time")
        f1 = str(start) +"T"+str(start_time) +":00"
        f2 = str(end) +"T"+str(end_time) +":00"
        #print(docId)
        print(label)
        print(value)
        print(f1)
        print(f2)
        api_deuda_new(idDeuda,f1,f2,value,label)

        return redirect('vent:deuda_list')


    context={
        'obj':docId,
        'docId':docId,
        'label':label,
        'payUrl':payUrl+"/qr",
        'value':value,
        'start':start,
        'end':end,
        'status':status,
        'fecha_actual':fecha_actual,
    }
    return render(request,template,context)

@login_required(login_url='/login/')
def deuda_delete(request,idDoc):
    api_deuda_delete(idDoc)
    list = api_deuda_list()

    template_name = 'deuda_list.html'
    messages.success(request, 'Eliminado correctamente')

    context={
        'obj':list,
    }
    return render(request,template_name,context)



@csrf_exempt
@require_POST
def webhook_endpoint(request):
    jsondata = request.body
    data = json.loads(jsondata)
    print(data)
    try:
        print(data["debt"])
        print(data["debt"]["docId"])
        print(data["debt"]["payStatus"]["status"])
        if data["debt"]["payStatus"]["status"] == "paid":
            LISTA_CAMBIOS[data["debt"]["docId"]] = data["debt"]["payStatus"]["status"]
        else:
            LISTA_CAMBIOS.pop(data["debt"]["docId"])
    except:
        pass

    return HttpResponse(status=200)

from rest_framework.views import APIView
from rest_framework import status

class Consult_pending(APIView):
    @csrf_exempt
    def get(self, request, format=None):
        try:
            idCode = request.GET.get('idCode')
            print(idCode)
        except:
            print("Revento al intentar leer el json")
            return Response({'message': 'Los datos recibidos no son correctos'},status = status.HTTP_400_BAD_REQUEST)
        try:
            LISTA_CAMBIOS[idCode]
            return Response({"message":"not"})
        except:
            return Response({"message":"yes"})

        return Response({"message":"ok"})
