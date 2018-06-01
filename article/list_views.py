from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import HttpResponse
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from .models import ArticleColumn,ArticlePost,Comment,CommentToComment,ArticleTag
from .forms import CommentForm
import redis
from django.conf import settings

r=redis.StrictRedis(host=settings.REDIS_HOST,port=settings.REIDS_PORT,db=settings.REDIS_DB)

def article_titles(request,username=None):
    if username:
        user=User.objects.get(username=username)
        articles_title=ArticlePost.objects.filter(author=user)
        try:
            userinfo=user.userinfo
        except:
            userinfo=None
    else:
        articles_title=ArticlePost.objects.all()

    if username:
        return render(request,'article/list/author_articles.html',{"articles":articles_title,
                                                                   "userinfo":userinfo,
                                                                   "user":user})
    return render(request,'article/list/article_titles.html',{'articles':articles_title})


@csrf_exempt
@login_required(login_url='/account/login/')
def article_detail(request,id,slug):
    article = get_object_or_404(ArticlePost, id=id, slug=slug)
    total_views = r.incr("article:{}:views".format(article.id))

    r.zincrby('article_ranking',article.id,1)
    article_ranking=r.zrange('article_ranking',0,-1,desc=True)[:10]
    article_ranking_ids = [int(id) for id in article_ranking]
    most_viewed = list(ArticlePost.objects.filter(id__in=article_ranking_ids))
    most_viewed.sort(key=lambda x: article_ranking_ids.index(x.id))

    if request.method == "POST":
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment=comment_form.save(commit=False)
            new_comment.article=article
            new_comment.commentator=request.user
            new_comment.save()
        elif request.POST['comment_id']:
            comment=Comment.objects.get(id=request.POST['comment_id'])
            new_comment = CommentToComment()
            new_comment.comment=comment
            new_comment.commentator=request.user
            new_comment.body=request.POST['bodys']
            if request.POST['comtocom_id'] == '-1':
                new_comment.commented=comment.commentator
            else:
                new_comment.commented = CommentToComment.objects.get(id=request.POST['comtocom_id']).commentator
            new_comment.save()
    else:
        comment_form = CommentForm()

    article_tags = article.article_tag.values_list("tag",flat=True)
    article_tag_ids=ArticleTag.objects.filter(tag__in=article_tags).values_list("id",flat=True)
    similar_articles = ArticlePost.objects.filter(article_tag__in=article_tag_ids).\
        exclude(id=article.id)
    similar_articles = similar_articles.annotate(same_tags=Count("article_tag")).order_by("-same_tags","-created")[:4]
    return render(request,"article/list/article_detail.html",{"article":article,"total_views":total_views,"most_viewed":most_viewed,"comment_form":comment_form,
                                                              "similar_articles":similar_articles})

@login_required(login_url='/account/login/')
@csrf_exempt
@require_POST
def like_article(request):
    article_id = request.POST.get('id')
    action = request.POST.get("action")
    if article_id and action:
        try:
            article = ArticlePost.objects.get(id=article_id)
            if action =='like':
                article.user_like.add(request.user)
                return HttpResponse('1')
            else:
                article.user_like.remove(request.user)
                return HttpResponse('2')
        except:
            return HttpResponse("no")