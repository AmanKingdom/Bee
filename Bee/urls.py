"""Bee URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path

from app.uploads import upload_image
from app.views import *

urlpatterns = [
    url(r'^$', homepage),

    url(r'^search/$', search, name='search'),
    url(r'^search_result/$', search_result),
    # 大众在Bee主页可见的博客文章具体内容页面对应网址
    url(r'^public-blog-article/(\d{0,100})/$', show_public_blog_article_content, name='public-blog-article-content'),

    url(r'^wechat-article/(\d{0,100})/$', show_wechat_article_content, name='wechat-article-content'),

    url(r'^login/$', login, name='login'),
    url(r'^logout/$', logout, name='logout'),
    url(r'^register/$', register, name='register'),
    url(r'^forget-password/$', forget_password, name='forget-password'),
    url(r'^user-homepage/$', user_homepage, name='user-homepage'),
    url(r'^my-blog-articles/$', my_blog_articles, name='my-blog-articles'),
    url(r'^my-fans/$', my_fans, name='my-fans'),
    url(r'^user-information/$', user_information, name='user-information'),
    url(r'^my-collections/$', my_collections, name='my-collections'),
    url(r'^my-attentions/$', my_attentions, name='my-attentions'),
    url(r'^write-blog-article/$', write_blog_article, name='write-blog-article'),
    url(r'^uploads/$', upload_image, name='upload_image'),
    # 个人登录后可见的自己博客文章具体内容页面对应网址
    url(r'^my-blog-article/(\d{0,10})/$', show_my_blog_article_content, name='my-blog-article-content'),
    url(r'^delete-blog-article/(.*?)/$', blog_article_delete, name='delete-blog-article'),

    path('admin/', admin.site.urls),

    url(r'^manage/$', manage, name='manage'),
    url(r'^manage/article-sort-design/$', article_sort_design, name='article-sort-design'),
    url(r'^manage/delete-sub-industry/(.*?)/$', sub_industry_delete, name='delete-sub-industry'),
    url(r'^manage/crawl-wechat-accounts/$', crawl_wechat_accounts, name='crawl-wechat-accounts'),
    url(r'^manage/delete-wechat-account/(.*?)/$', delete_wechat_account, name='delete-wechat-account'),

    url(r'^manage/show-wechat-articles/$', show_wechat_articles, name='show-wechat-articles'),
    url(r'^manage/crawl-articles/$', crawl_articles, name='crawl-articles'),
    url(r'^manage/crawl-wechat-articles/(.*?)/$', crawl_wechat_articles, name='crawl-wechat-articles'),
    url(r'^manage/delete-wechat-article/(.*?)/$', delete_wechat_article, name='delete-wechat-article'),
]
