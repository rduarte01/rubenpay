from django.urls import path, reverse_lazy
from .views import *


urlpatterns = [
    path('deudas/', deuda_list, name="deuda_list"),
    path('deudas/new', deuda_new, name="deuda_new"),
    path('deudas/edit/<str:idDoc>', deuda_edit, name="deuda_edit"),

]