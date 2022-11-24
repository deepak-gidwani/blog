from django.http import Http404, HttpResponse 
from django.shortcuts import render , get_object_or_404, redirect
from django.http import HttpResponse
from django.http import Http404
from .models import Post
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormView, CreateView
from django.views import View
from django.urls import reverse
from .forms import CommentForm

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

# class SinglePostView(DetailView): using normal view for get and post both
#     template_name = "blog/post-detail.html"
#     model = Post
#     context_object_name = "post"

#     def get_context_data(self, **kwargs):
#         context =  super().get_context_data(**kwargs)
#         context["post_tags"] = self.object.tags.all()
#         context["comment_form"] = CommentForm()
#         return context

class SinglePostView(View): 
    def get(self,request,slug):
        context = self.common(slug)
        stored_posts = request.session.get("stored_posts")
        if stored_posts is not None:
            is_saved_for_later = context["post"].id in stored_posts
        else:
            is_saved_for_later = False
        context["saved_for_later"]=is_saved_for_later
        return render(request,"blog/post-detail.html",context)


    def post(self,request,slug):
        # comment_form = CommentForm(request.POST)  in sb ko fxn m daal diya
        # post = Post.objects.get(slug=slug)
        # post_tags = post.tags.all()
        # comments = post.comments.all()

        context = self.common(slug)
        context["comment_form"] = CommentForm(request.POST)
        if context["comment_form"].is_valid():
            # print(request.POST)  request.post is a dictionary
            comment = context["comment_form"].save(commit=False)  # ye abhi database hit hone se rokega infact ye new model instance bnaega so store in some variable
            comment.post = context["post"]  # manually saving post
            comment.save()
            return redirect(reverse("post-detail-page",args=[slug]))

        stored_posts = request.session.get("stored_posts")
        if stored_posts is not None:
            is_saved_for_later = context["post"].id in stored_posts
        else:
            is_saved_for_later = False
        context["saved_for_later"]=is_saved_for_later

        return render(request,"blog/post-detail.html",context)

    def common(self,slug):
        post = Post.objects.get(slug=slug)
        post_tags = post.tags.all()
        comment_form = CommentForm()
        comment = post.comments.all().order_by("-id")
        context = {
            "post":post,
            "post_tags":post_tags,
            "comment_form":comment_form,
            "comments":comment
        }
        return context

class ReadLaterView(View):
    def get(self,request):
        stored_posts = request.session.get("stored_posts")

        context = {}
        if stored_posts is None or len(stored_posts)==0:
            context["posts"] = []
            context["has_posts"] = False
        else:
            posts = Post.objects.filter(id__in=stored_posts) #imp
            context["posts"] = posts
            context["has_posts"] = True
        
        return render(request,"blog/stored-post.html",context)

    def post(self,request):
        stored_posts = request.session.get("stored_posts")

        if stored_posts is None:
            stored_posts = []

        post_id = int(request.POST["post_id"])

        if post_id not in stored_posts:
            stored_posts.append(post_id) 
        else:
            stored_posts.remove(post_id) 
        
        request.session["stored_posts"] = stored_posts  #updating session
        return redirect("/")
    




# def post_details(request, slug):
#     try:
#         identified_post = get_object_or_404(Post, slug=slug)
#         return render(request, "blog/post-detail.html" ,{
#             "post":identified_post,
#             "post_tags":identified_post.tags.all()
#         })
#     except:
#         raise Http404()

