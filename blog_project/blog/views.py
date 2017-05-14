# encoding:utf-8
from django.shortcuts import render
from django.conf import settings
from .models import Category,Article, Ad
from django.core.paginator import Paginator, EmptyPage, InvalidPage, PageNotAnInteger
import logging


logging.getLogger('blog.views')

def global_settings(request):
    category_list = Category.objects.all()
    archive_list = Article.objects.distinct_date() 
    ad_list = Ad.objects.all()
    #article = Article.objects.all()
    return {
        'ad_list': ad_list,
        'category_list': category_list, 
        'archive_list': archive_list,
        #'article': article,
        'SITE_NAME': settings.SITE_NAME,
        'SITE_DESC': settings.SITE_DESC,
        'GITHUb_URL': settings.GITHUB_URL,
    }
def get_page(request, article_list):
    paginator = Paginator(article_list, 3)
    try:
        page = int(request.GET.get('page', 1))
        article_list = paginator.page(page)
    except Exception:
        article_list = paginator.page(1)

    return article_list

def index(request):
    # 分页
    article_list = get_page(request, Article.objects.all())
    # 广告
    ad_list = Ad.objects.all()
    # 分类
    return render(request, 'index.html', locals())

def article(request):
    id = request.GET.get('id', None)
    try:
        article = Article.objects.get(id=id)
    except Exception as e:
        logging.error(e)
    return render(request, 'article.html', locals())

# 分类
def category(request):
    cid = request.GET.get('cid', None)
    try:
        category = Category.objects.get(id=cid)
    except Category.DoesNotExist:
        return render('failure.html', {'reason': '分类不存在'})
    except Exception as e:
        logging.error(e)
    article_list = get_page(request, Article.objects.filter(category=category))
    return render(request, 'category.html', locals())

def archive(request):
    try:
        # 文章归档
        archive = Article.objects.distinct_date() 
        article_list = get_page(request, Article.objects.all())
    except Exception as e:
        logging.error(e)
    return render(request, 'archive.html', locals())
def ad(request):
    try:
        ad_list = Ad.objects.all()
        logging.error('ad_list.image_url:',ad_list.image_url)
    except Exception as e:
        logging.error(e)
    return render(request, 'ad.html', locals()) 

