from django.urls import path, reverse_lazy
from .views import *


urlpatterns = [
    path('deudas/', deuda_list, name="deuda_list"),
    path('deudas/new', deuda_new, name="deuda_new"),
    path('deudas/edit/', deuda_list, name="deuda_edit"),

]