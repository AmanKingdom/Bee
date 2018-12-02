import os
import re

from django.http import HttpResponseRedirect
from django.shortcuts import render
from app.forms import *
from app.models import WechatAccount, Carousel
from engine.Wechat_SQLite.search_sqlite import Search
import datetime
from engine.Wechat_SQLite.spider_sqlite import *

# 主页
def homepage(request):
    if 'user_id' in request.session:
        user_id = request.session['user_id']
    blog_articles = BlogArticle.objects.all()
    wechat_articles = WeChatArticle.objects.all()[0:15]

    # 轮播图
    carousel = Carousel.objects.all().order_by('number')
    # 需要用到轮播图的数量
    carousel_len = [x for x in range(0, len(carousel))]
    if len(carousel) is 0:
        carousel = None

    now = datetime.datetime.now()
    # template = get_template('users-window/index.html')
    # html = template.render(locals())
    # return HttpResponse(html)
    return render(request, 'users-window/index.html', locals())


# 主页上的公开博客文章列表项点击后跳转的具体内容页
def show_public_blog_article_content(request, article_id):
    if 'user_id' in request.session:
        user_id = request.session['user_id']
    blog_article = BlogArticle.objects.get(id=int(article_id))
    return render(request, 'users-window/public-blog-article-content.html', locals())

# 主页上搜索时的接收关键字方法
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

# 主页上接收关键字后的搜索方法，并跳转到搜索结果页面
def search_result(request):
    if 'user_id' in request.session:
        user_id = request.session['user_id']
    if 'search_key' in request.session:
        search_text = request.session['search_key']
        print('正在搜索：', search_text, '……')

        search_results = Search(search_text).search_infos()

        if len(search_results) == 0:
            search_results = None
            print('搜索“', search_text, '”时，并没有找到什么。')
        else:
            # 通过搜索结果列表中各项的公众号id获取公众号名称
            wechat_name_list = [WechatAccount.objects.get(wechat_id=x.get('wechat_id')).wechat_name for x in search_results]
            # 通过搜索结果列表中各项的文章id获取对应的文章对象
            wechat_articles = [WeChatArticle.objects.get(id=x.get('article_id')) for x in search_results]

            # 打包发送到templates让它自己解压处理
            articles_list = zip(search_results, wechat_name_list, wechat_articles)
    else:
        return HttpResponseRedirect('/')
    return render(request, 'users-window/search-result.html', locals())

# 展示指定微信文章的具体内容的方法
def show_wechat_article_content(request, article_id):
    if 'user_id' in request.session:
        user_id = request.session['user_id']
    wechat_article = WeChatArticle.objects.get(id=int(article_id))
    return render(request, 'users-window/wechat-article-page.html', locals())


# 用户退出登录的方法
def logout(request):
    # session中的内容并不需要判断存不存在
    request.session['user_id'] = None
    return HttpResponseRedirect('/login/')

# 用户个人信息的显示方法
def user_information(request):
    if 'user_id' in request.session:
        user_id = request.session['user_id']
        user = User.objects.get(user_id=user_id)
    else:
        return HttpResponseRedirect('/login/')
    return render(request, 'users-window/user-information.html', locals())

# 用户登录后才能看到的个人文章列表的显示方法
def my_blog_articles(request):
    if 'user_id' in request.session:
        user_id = request.session['user_id']
        user = User.objects.get(user_id=user_id)
        blog_articles = user.blogarticle_set.all()
    else:
        return HttpResponseRedirect('/login/')
    return render(request, 'users-window/my-blog-article.html', locals())

# 用户的关注内容的显示方法
def my_attentions(request):
    if 'user_id' in request.session:
        user_id = request.session['user_id']
    else:
        return HttpResponseRedirect('/login/')
    return render(request, 'users-window/my-attentions.html', locals())

# 用户的收藏内容的显示方法
def my_collections(request):
    if 'user_id' in request.session:
        user_id = request.session['user_id']
    else:
        return HttpResponseRedirect('/login/')
    return render(request, 'users-window/my-collections.html', locals())

# 用户的粉丝的显示方法
def my_fans(request):
    if 'user_id' in request.session:
        user_id = request.session['user_id']
    else:
        return HttpResponseRedirect('/login/')
    return render(request, 'users-window/my-fans.html', locals())

# 用户登录后的博客文章创作页面的显示方法
def write_blog_article(request):
    if 'user_id' in request.session:
        user_id = request.session['user_id']
        article_form = BlogArticleForm()
        if request.method == 'POST':
            print("博客文章提交了,方式为POST。")

            article_form = BlogArticleForm(request.POST)
            if article_form.is_valid():
                article_content = article_form.data.get('article_content')
                # flag可以用来标记是否有视频存在，还可以标记有多少个视频
                flag = 0
                if '<embed' in article_content:
                    # 检查到有视频输入
                    urls = re.findall('<embed src="/static/media/upload/(.*?)"', article_content)
                    print('博客文章中有视频，视频文件为：', urls)

                    for url in urls:
                        if os.path.exists('./static/media/upload/' + url):
                            print('文件存在')
                            flag = flag + 1
                        else:
                            print('文件不存在，继续执行可能会出错')
                article_form.instance.author = User.objects.get(user_id=user_id)
                title = article_form.save()
                if flag > 0:
                    embed_labels_attr = iter(re.findall('<embed src="/static/media/upload/(.*?)/>', article_content, re.S))
                    for i in range(0, flag):
                        article_content = re.sub(pattern='<embed src="/static/media/upload/.*?/>', repl='<iframe src="/static/media/upload/%s></iframe>' % next(embed_labels_attr), string=article_content)
                    BlogArticle.objects.filter(article_title=title).update(article_content=article_content)
                return HttpResponseRedirect('/write-blog-article/')
    else:
        return HttpResponseRedirect('/login/')
    return render(request, 'users-window/write-blog-article.html', locals())

# 用户登录后用于展示用户个人文章具体内容的方法
def show_my_blog_article_content(request, article_id):
    if 'user_id' in request.session:
        user_id = request.session['user_id']
        blog_article = BlogArticle.objects.get(id=int(article_id))
    else:
        return HttpResponseRedirect('/login/')
    return render(request, 'users-window/my-blog-article-page.html', locals())

# 用户登录后才能删除用户个人文章的显示方法
def blog_article_delete(request, article_title):
    BlogArticle.objects.filter(article_title=article_title).delete()
    return HttpResponseRedirect('/my-blog-articles/')

# 用户登录后的个人主页的显示方法
def user_homepage(request):
    if 'user_id' in request.session:
        user_id = request.session['user_id']
    else:
        return HttpResponseRedirect('/login/')
    return render(request, 'users-window/user-homepage.html', locals())

# 用户的登录界面的方法
def login(request):
    request.session['user_id'] = None
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
                return HttpResponseRedirect('/user-information/')
            elif login_user_form.data.get('user_id') == u.user_id and login_user_form.data.get('password') != u.password:
                feedback_message = '密码不对哦大哥'
                break
            else:
                feedback_message = '您还没注册吧？点击下方链接注册一下？或者检查一下您的账号是否写对哦'

    return render(request, 'users-window/login.html', locals())

# 用户账户注册界面的显示方法
def register(request):
    request.session['user_id'] = None
    register_user = UserRegisterForm()
    if request.method == 'POST':
        register_user = UserRegisterForm(request.POST)
        if register_user.is_valid():
            print(register_user.data)
            register_user.save()
            return HttpResponseRedirect('/login/')
    return render(request, 'users-window/register.html', locals())

def forget_password(request):
    request.session['user_id'] = None
    return render(request, 'users-window/forget-password.html', locals())




# 后台用户管理界面的显示方法
def manage(request):
    return render(request, 'manage-window/index.html', locals())

# 后台用户管理的文章分类设计页面的显示方法
def article_sort_design(request):
    industry_form = IndustryForm()
    if request.method == 'POST':
        industry_form = IndustryForm(request.POST)
        if industry_form.is_valid():
            industry_form.save()
            return HttpResponseRedirect('/manage/article-sort-design/')
    industry_dict = get_industry_dict()
    return render(request, 'manage-window/article-sort-design.html', locals())

# 转化数据库中领域表的信息为字典的方法
def get_industry_dict():
    industrys = Industry.objects.all()
    industry_dict = {}
    for item in industrys:
        if item.industry_name not in industry_dict.keys():
            industry_dict[item.industry_name] = [item.sub_industry_name]
        else:
            industry_dict[item.industry_name].append(item.sub_industry_name)
    return industry_dict

# 删除子领域的方法
def sub_industry_delete(request, sub_industry_name):
    Industry.objects.filter(sub_industry_name=sub_industry_name).delete()
    return HttpResponseRedirect('/manage/article-sort-design/')

def crawl_articles(request):
    return render(request, 'manage-window/crawl.html', locals())

def crawl_wechat_accounts(request):
    wechat_accounts = WechatAccount.objects.all()
    wechat_ids = []

    if request.method == 'POST':
        wechat_id_dict = request.POST
        print('接收到前端的原始数据：', wechat_id_dict)
        # 以逗号为分割符分割该字符串
        wechat_ids = str(wechat_id_dict['wechat-account-id']).split(',')
        if wechat_ids is not None:
            print('分割后的数据列表：', wechat_ids)

            wechat_account_info = AccountSpider(wechat_ids).get_account_infos()
            print('爬取成功的公众号为：', wechat_account_info)
    return render(request, 'manage-window/crawl-wechat-accounts.html', locals())

def delete_wechat_account(request, wechat_id):
    # 需要连着头像一起删除，这里[1:]的意思是去掉开头的'/'，这样才能找到对的路径
    account = WechatAccount.objects.get(wechat_id=wechat_id)
    head_portrait = account.head_portrait[1:]
    qr_code = account.qr_code[1:]
    print('删除的头像路径为', head_portrait)
    if os.path.exists(head_portrait):
        os.remove(head_portrait)
        os.remove(qr_code)
        print('成功删除路径为', head_portrait, '的头像和路径为', qr_code, '的二维码。')
        # os.unlink(my_file)    # <——也可以用这个语句删除
    else:
        print('文件不存在，不需要删除。')
    WechatAccount.objects.filter(wechat_id=wechat_id).delete()
    return HttpResponseRedirect('/manage/crawl-wechat-accounts/')


# 这个是爬取文章的根方法
def crawl_articles(request):
    accounts = WechatAccount.objects.all()
    wechat_articles = WeChatArticle.objects.all()
    if request.method == 'POST':
        crawl_accounts = request.POST.getlist('selected_accounts')
        print('接收到要爬取的公众号列表：', crawl_accounts)
        ArticleSpider(crawl_accounts).get_infos()
        message = '爬取完毕，请刷新网页'
    if 'wechat_id' in request.session:
        wechat_id = request.session['wechat_id']
        print('接收到session：wechat_id:', wechat_id)
        if wechat_id is None:
            return render(request, 'manage-window/crawl-wechat-articles.html', locals())
        else:
            wechat_ids = []
            wechat_ids.append(wechat_id)
            ArticleSpider(wechat_ids).get_infos()
            request.session['wechat_id'] = None
    else:
        print('仅打开了爬文章页面。')

    wechat_articles = WeChatArticle.objects.all()
    return render(request, 'manage-window/crawl-wechat-articles.html', locals())

def crawl_wechat_articles(request, wechat_id):
    if request.method == 'POST':
        if wechat_id == 'all':
            print('即将爬取库里所有公众号的文章……')
            all_accounts = [x.wechat_id for x in WechatAccount.objects.all()]
            print('目前的所有公众号为：', all_accounts)
            ArticleSpider(all_accounts).get_infos()
            message = '爬取完毕。'
            print(message)
            return HttpResponseRedirect('/manage/crawl-articles/')
    else:
        request.session['wechat_id'] = wechat_id
    return HttpResponseRedirect('/manage/crawl-articles/')

def delete_wechat_article(request, article_id):
    WeChatArticle.objects.filter(id=article_id).delete()
    return HttpResponseRedirect('/manage/show-wechat-articles/')

def show_wechat_articles(request):
    wechat_articles = WeChatArticle.objects.all()
    return render(request, 'manage-window/show-wechat-articles.html', locals())

def manage_carousel(request):
    current_carousels = Carousel.objects.all().order_by('number')
    wechat_articles = WeChatArticle.objects.all()
    return render(request, 'manage-window/manage-carousel.html', locals())

def add_wechat_article_to_carousel(request, article_id):
    wechat_article = WeChatArticle.objects.get(id=article_id)
    carousel_len = len(Carousel.objects.all())
    print('目前轮播图的个数为：', carousel_len)
    Carousel.objects.create(img_url=wechat_article.cover_img, title=wechat_article.article_title, article_url=wechat_article.id, alt=wechat_article.article_title, number=carousel_len)
    return HttpResponseRedirect('/manage/manage-carousel/')

def delete_carousel(request, id):
    number = Carousel.objects.get(id=id).number
    Carousel.objects.filter(id=id).delete()
    carousel_list = Carousel.objects.all().order_by('number')
    for i in carousel_list:
        print('取出的轮播对象的序号：', i.number)
        if i.number > number:
            Carousel.objects.filter(id=i.id).update(number=(i.number-1))

    return HttpResponseRedirect('/manage/manage-carousel/')

def carousel_up(request, number):
    number = int(number)
    print('上移的轮播图序号：', number)
    if number == 0:
        return HttpResponseRedirect('/manage/manage-carousel/')
    elif number > 0:
        # 要上移的对象
        up_carousel = Carousel.objects.get(number=number)
        # 和要上移对象的上一个对象交换序号
        Carousel.objects.filter(number=(number-1)).update(number=number)
        Carousel.objects.filter(id=up_carousel.id).update(number=(number-1))
    else:
        print('轮播图的序号number为负数？')
    return HttpResponseRedirect('/manage/manage-carousel/')

def carousel_down(request, number):
    number = int(number)
    print('下移的轮播图序号：', number)
    if number == len(Carousel.objects.all()):
        return HttpResponseRedirect('/manage/manage-carousel/')
    elif number >= 0:
        # 要下移的对象
        down_carousel = Carousel.objects.get(number=number)
        # 和要下移对象的下一个对象交换序号
        Carousel.objects.filter(number=(number + 1)).update(number=number)
        Carousel.objects.filter(id=down_carousel.id).update(number=(number + 1))
    else:
        print('number为负数？')
    return HttpResponseRedirect('/manage/manage-carousel/')
