# encoding:utf-8
from django.shortcuts import render
from django.conf import settings
from .models import Category,Article
from django.core.paginator import Paginator, EmptyPage, InvalidPage, PageNotAnInteger
import logging


logging.getLogger('blog.views')

def global_settings(request):
    return {
        'SITE_NAME':settings.SITE_NAME,
        'SITE_DESC':settings.SITE_DESC,
        'GITHUb_URL':settings.GITHUB_URL,
    }
def index(request):
    try:
        # 广告
        # 分页
        # 分类
        category_list = Category.objects.all()
        paginator = Paginator(Article.objects.all(), 2)
        page = int(request.GET.get('page', 1))
        article_list = paginator.page(page)

    except (EmptyPage, InvalidPage, PageNotAnInteger):
        article_list = paginator.page(1)
        #logging.error(e)
    #return render(request, 'index.html', {'category_list':category_list})
    return render(request, 'index.html', locals())

def article(request):
    try:
        # 分类
        article_list = Article.objects.all()
    except Exception as e:
        logging.error(e)
    return render(request, 'article.html', locals())

def category(request):
    try:
        # 分类
        category_list = Category.objects.all()
    except Exception as e:
        logging.error(e)
    return render(request, 'category.html', locals())

def archive(request):
    try:
        # 文章归档
        archive_list = Article.objects.distinct_date() 
    except Exception as e:
        logging.error(e)
    return render(request, 'archive.html', locals())
