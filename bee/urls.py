"""bee URL Configuration

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
from app.uploads import upload_image
from app.views import *

urlpatterns = [
    url(r'^$', homepage),

    url(r'^search/$', search, name='search'),
    url(r'^search_result/$', search_result),
    url(r'^wechat-article/(\d{0,100})/$', show_wechat_article_content, name='wechat-article-content'),

    url(r'^write-blog-article/$', write_blog_article, name='write-blog-article'),
    url(r'^uploads/$', upload_image, name='upload_image'),
    url(r'^blog-article/(\d{0,100})/$', show_blog_article_page, name='blog-article-content'),
    url(r'^delete-blog-article/(.*?)/$', blog_article_delete, name='delete-blog-article'),

    url(r'^login/$', login, name='login'),
    url(r'^logout/$', logout, name='logout'),
    url(r'^register/$', register, name='register'),
    url(r'^user-homepage/$', user_homepage, name='user-homepage'),
    url(r'^my-blog-articles/$', my_blog_articles, name='my-blog-articles'),
    url(r'^my-fans/$', my_fans, name='my-fans'),
    url(r'^user-information/$', user_information, name='user-information'),
    url(r'^my-collections/$', my_collections, name='my-collections'),
    url(r'^my-attentions/$', my_attentions, name='my-attentions'),

    url(r'^admin/', admin.site.urls),

    url(r'^manage/$', manage),
    url(r'^manage/article-sort-design/$', article_sort_design, name='article-sort-design'),
    url(r'^manage/delete-sub-industry/(.*?)/$', sub_industry_delete, name='delete-sub-industry'),
]
