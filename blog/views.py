from django.http import Http404, HttpResponse 
from django.shortcuts import render , get_object_or_404
from django.http import HttpResponse
from django.http import Http404
from .models import Post

# Create your views here.

all_posts = Post.objects.all().order_by("-date")

# def get_date(post):  # helper function for sorting data acc to date
#     return post['date']

def starting_page(request):
    
    latest_post = Post.objects.all().order_by("-date")[:3]  # sort in descending order
    return render(request, "blog/index.html",{
        "posts" : latest_post
    })


def posts(request):
    return render(request, "blog/all-posts.html",{
        "all_posts":all_posts
    })


def post_details(request, slug):
    try:
        identified_post = get_object_or_404(Post, slug=slug)
        return render(request, "blog/post-detail.html" ,{
            "post":identified_post,
            "post_tags":identified_post.tags.all()
        })
    except:
        raise Http404()

