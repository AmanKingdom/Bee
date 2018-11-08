import os
import re

from django.http import HttpResponseRedirect
from django.shortcuts import render

from app.forms import *
from spider.Wechat_SQLite.search_sqlite import Search


def homepage(request):
    if 'user_id' in request.session:
        user_id = request.session['user_id']
    blog_articles = BlogArticle.objects.all()
    wechat_articles = WeChatArticle.objects.all()[0:15]

    return render(request, 'users-window/index.html', locals())


def search(request):
    try:
        search_key = request.GET['search-text']
    except:
        search_key = None
    if search_key is "":
        return HttpResponseRedirect('/')
    else:
        request.session['search_key'] = search_key
        return HttpResponseRedirect('/search_result/')

def search_result(request):
    if 'search_key' in request.session:
        search_text = request.session['search_key']
        print('正在搜索：', search_text, '……')

        wechat_articles = Search(search_text).search_infos()
        print('\n\n\n\n\n wechat_article的内容：', wechat_articles)

        if len(wechat_articles) == 0:
            print('没有找到什么')
            return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/')
    return render(request, 'users-window/search-result.html', locals())

def show_wechat_article_content(request, article_id):
    wechat_article = WeChatArticle.objects.get(id=int(article_id))
    return render(request, 'users-window/wechat-article-page.html', locals())


def logout(request):
    request.session['user_id'] = None
    return HttpResponseRedirect('/')


def my_blog_articles(request):
    blog_articles = BlogArticle.objects.all()
    return render(request, 'users-window/my-blog-article.html', locals())


def my_fans(request):
    return render(request, 'users-window/my-fans.html', locals())

def write_blog_article(request):
    article_form = BlogArticleForm()
    if request.method == 'POST':
        print("提交方式为POST。")
        article_form = BlogArticleForm(request.POST)
        if article_form.is_valid():
            article_content = article_form.data.get('article_content')
            if '<embed' in article_content:
                # 检查是不是有视频输入
                urls = re.findall('<embed src="/static/media/upload/(.*?)"', article_content)
                print('博客文章中有视频，视频文件为：', urls)
                # flag可以用来标记是否有文件存在，还可以标记有多少个文件
                flag = 0
                for url in urls:
                    if os.path.exists('./static/media/upload/' + url):
                        print('文件存在')
                        flag = flag + 1
                    else:
                        print('文件不存在，继续执行可能会出错')
                if flag > 0:
                    embed_labels_attr = iter(re.findall('<embed src="/static/media/upload/(.*?)/>', article_content, re.S))
                    for i in range(0, flag):
                        article_content = re.sub(pattern='<embed src="/static/media/upload/.*?/>', repl='<iframe src="/static/media/upload/%s></iframe>' % next(embed_labels_attr), string=article_content)
                title = article_form.save()
                print('embed标签转化为iframe标签后的文章HTML代码：', article_content)
                article = BlogArticle.objects.filter(article_title=title).update(article_content=article_content)
            else:
                article_form.save()
            return HttpResponseRedirect('/write-blog-article/')
    return render(request, 'users-window/write-blog-article.html', locals())

def show_blog_article_page(request, article_id):
    blog_article = BlogArticle.objects.get(id=int(article_id))
    return render(request, 'users-window/blog-article-page.html', locals())

def blog_article_delete(request, article_title):
    BlogArticle.objects.filter(article_title=article_title).delete()
    return HttpResponseRedirect('/blog-page/')

def user_homepage(request):
    if 'user_id' in request.session:
        user_id = request.session['user_id']
        print('收到user_id:',user_id)
    return render(request, 'users-window/user-homepage.html', locals())

def login(request):
    feedback_message = None
    # 显示到登录页面的:登录用户模型
    user = UserLoginForm()
    if request.method == 'POST':
        # 获取当前输入的信息并与数据库所有用户信息做比较
        login_user_form = UserLoginForm(request.POST)
        for u in User.objects.all():
            if login_user_form.data.get('user_id') == u.user_id and login_user_form.data.get('password') == u.password:
                feedback_message = '登录成功啦'
                request.session['user_id'] = u.user_id
                return HttpResponseRedirect('/user-homepage/')
            elif login_user_form.data.get('user_id') == u.user_id and login_user_form.data.get('password') != u.password:
                feedback_message = '密码不对哦大哥'
                break
            else:
                feedback_message = '您还没注册吧？点击下方链接注册一下？或者检查一下您的账号是否写对哦'

    return render(request, 'users-window/login.html', locals())


def register(request):
    register_user = UserRegisterForm()
    if request.method == 'POST':
        register_user = UserRegisterForm(request.POST)
        if register_user.is_valid():
            print(register_user.data)
            register_user.save()
            return HttpResponseRedirect('/login/')
    return render(request, 'users-window/register.html', locals())

def manage(request):
    return render(request, 'manage-window/index.html', locals())

def article_sort_design(request):
    industry_form = IndustryForm()
    if request.method == 'POST':
        industry_form = IndustryForm(request.POST)
        if industry_form.is_valid():
            industry_form.save()
            return HttpResponseRedirect('/manage/article-sort-design/')
    industry_dict = get_industry_dict()
    return render(request, 'manage-window/article-sort-design.html', locals())


def get_industry_dict():
    industrys = Industry.objects.all()
    industry_dict = {}
    for item in industrys:
        if item.industry_name not in industry_dict.keys():
            industry_dict[item.industry_name] = [item.sub_industry_name]
        else:
            industry_dict[item.industry_name].append(item.sub_industry_name)
    return industry_dict

def sub_industry_delete(request, sub_industry_name):
    Industry.objects.filter(sub_industry_name=sub_industry_name).delete()
    return HttpResponseRedirect('/manage/article-sort-design/')
