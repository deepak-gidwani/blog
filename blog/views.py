from django.http import Http404, HttpResponse 
from django.shortcuts import render , get_object_or_404
from django.http import HttpResponse
from django.http import Http404
from .models import Post
from django.views.generic import ListView, DetailView
# Create your views here.

all_posts = Post.objects.all().order_by("-date")

# def get_date(post):  # helper function for sorting data acc to date
#     return post['date']

# def starting_page(request):
    
#     latest_post = Post.objects.all().order_by("-date")[:3]  # sort in descending order
#     return render(request, "blog/index.html",{
#         "posts" : latest_post
#     })
class StartingPageView(ListView):
    template_name = "blog/index.html"
    model = Post
    context_object_name = "posts"
    ordering = ["-date"][:3]
    def get_queryset(self):
        context = super().get_queryset()
        # context = context.order_by("-date")[:2] iski jgh ordering field use krliya 
        return context


class AllPostView(ListView):
    template_name = "blog/all-posts.html"
    model = Post
    context_object_name = "all_posts"
# def posts(request):
#     return render(request, "blog/all-posts.html",{
#         "all_posts":all_posts
#     })

class SinglePostView(DetailView):
    template_name = "blog/post-detail.html"
    model = Post
    context_object_name = "post"

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context["post_tags"] = self.object.tags.all()
        return context

# def post_details(request, slug):
#     try:
#         identified_post = get_object_or_404(Post, slug=slug)
#         return render(request, "blog/post-detail.html" ,{
#             "post":identified_post,
#             "post_tags":identified_post.tags.all()
#         })
#     except:
#         raise Http404()

