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
from vent.api import *

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

    if request.method == "POST":

        docId  = request.POST.get("docId")

        return redirect('vent:deuda_list')


    context={
        'obj':None,
    }
    return render(request,template,context)