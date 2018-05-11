from django.shortcuts import render,get_object_or_404
from .models import BlogArticles

# Create your views here.

def blog_title(request):
    blogs=BlogArticles.objects.all()
    return render(request,"blog/titles.html",{'blogs':blogs})

def blog_article(request,article_id):
    #blog=BlogArticles.objects.get(id=article_id)
    blog=get_object_or_404(BlogArticles,id=article_id)
    pub=blog.publish
    return render(request,"blog/content.html",{'blog':blog,"publish":pub})

