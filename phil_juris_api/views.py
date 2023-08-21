from django.shortcuts import render
from django.http import HttpResponse
from pyrebase.pyrebase import *

# Create your views here.
def index(request):
    return HttpResponse("<h1>Philippine Jurisprudence API<h1>")