from django.shortcuts import render
from django.http import HttpResponse


def home(request):
    return HttpResponse('<h1> blog home</h1>')


def about(request):
    return HttpResponse('<h1> blog aabut</h1>')
# Create your views here.