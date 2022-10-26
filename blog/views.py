from django.http import HttpResponse
from django.shortcuts import render
from django.http import HttpResponse 

# Create your views here.

def starting_page(request):
    return render(request,"blog/index.html")

def posts(request):
    return HttpResponse("posts")

def post_details(request):
    return HttpResponse("post-details")