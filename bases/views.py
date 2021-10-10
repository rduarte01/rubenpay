from datetime import datetime
from random import randint

from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import   generic
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt



class MixinFormInvalid:
    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors,status=400)
        else:
            return response

class SinPrivilegios(LoginRequiredMixin,MixinFormInvalid,PermissionRequiredMixin):
    login_url = 'bases:login'
    raise_exception = False
    redirect_field_name = "redirect_to"

    def __init__(self):
        self.request = None

    def handle_no_permission(self):
        from django.contrib.auth.models import AnonymousUser
        if not self.request.user==AnonymousUser():
            self.login_url='bases:sin_privilegios'
        return HttpResponseRedirect(reverse_lazy(self.login_url))
import datetime
#mixin siempre a la izquierda, hereda de ambos
class Home(LoginRequiredMixin, generic.TemplateView):
    template_name = 'bases/home.html'
    login_url = 'bases:login'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context


class HomeSinPrivilegios(LoginRequiredMixin,generic.TemplateView):
    login_url = 'bases:login'
    template_name = "bases/sin_privilegios.html"



