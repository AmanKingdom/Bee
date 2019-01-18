import datetime

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.template.loader import get_template
from django.views.decorators.csrf import csrf_exempt

from app.forms import *
from app.models import *
from engine.Wechat_SQLite.search_sqlite import Search
from engine.Wechat_SQLite.spider_sqlite import *
from engine.similarity_judgment.similarity import SimilarityJudge

# 主页
def homepage(request):
    if 'user_id' in request.session:
        user_id = request.session['user_id']
    else:
        user_id = None
    blog_articles = BlogArticle.objects.all()
    wechat_articles = WeChatArticle.objects.all().order_by('-publish_date')[0:15]

    # 十大校园组织的文章
    ten_organizations = WeChatArticle.objects.filter(wechat='dglgxyxsh').order_by('-publish_date')[0:13]

    # 轮播图
    carousel = Carousel.objects.all().order_by('number')
    # 需要用到轮播图的数量
    carousel_len = [x for x in range(0, len(carousel))]
    if len(carousel) is 0:
        carousel = None

    on_wall_articles = [x.article for x in OnWall.objects.filter(pass_or_not=True)]

    now = datetime.datetime.now()

    return_info = {'user_id': user_id, 'blog_articles': blog_articles, 'wechat_articles': wechat_articles,
                   'ten_organizations': ten_organizations, 'carousel': carousel, 'carousel_len': carousel_len,
                   'on_wall_articles': on_wall_articles, 'now': now}
    html = get_template('users-window/index.html').render(return_info)
    return HttpResponse(html)


# 主页上的公开博客文章列表项点击后跳转的具体内容页
def show_public_blog_article_content(request, article_id):
    if 'user_id' in request.session:
        user_id = request.session['user_id']
    else:
        user_id = None
    blog_article = BlogArticle.objects.get(id=int(article_id))
    BlogArticle.objects.filter(id=int(article_id)).update(browsed_times=blog_article.browsed_times+1)
    blog_article = BlogArticle.objects.get(id=int(article_id))

    return_info = {'user_id': user_id, 'blog_article': blog_article}
    html = get_template('users-window/public-blog-article-content.html').render(return_info)
    return HttpResponse(html)

# 主页上搜索时的接收关键字方法
def search(request):
    try:
        search_key = request.GET['search-text']
        if search_key is "":
            return HttpResponseRedirect('/')
        else:
            request.session['search_key'] = search_key
            return HttpResponseRedirect('/search_result/')
    except:
        return HttpResponseRedirect('/')

# 主页上接收关键字后的搜索方法，并跳转到搜索结果页面
def search_result(request):
    if 'user_id' in request.session:
        user_id = request.session['user_id']
    else:
        user_id = None
    if 'search_key' in request.session:
        search_text = request.session['search_key']

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

            return_info = {'user_id': user_id, 'articles_list': articles_list}
            html = get_template('users-window/search-result.html').render(return_info)
            return HttpResponse(html)

        return_info = {'user_id': user_id}
        html = get_template('users-window/search-result.html').render(return_info)
        return HttpResponse(html)
    else:
        return HttpResponseRedirect('/')

# 展示指定微信文章的具体内容的方法
def show_wechat_article_content(request, article_id):
    if 'user_id' in request.session:
        user_id = request.session['user_id']
    else:
        user_id = None
    wechat_article = WeChatArticle.objects.get(id=int(article_id))

    return_info = {'user_id': user_id, 'wechat_article': wechat_article}
    html = get_template('users-window/wechat-article-page.html').render(return_info)
    return HttpResponse(html)

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
    return_info = {'user_id': user_id, 'user': user}
    html = get_template('users-window/user-information.html').render(return_info)
    return HttpResponse(html)

# 用户登录后才能看到的个人文章列表的显示方法
def my_blog_articles(request):
    if 'user_id' in request.session:
        user_id = request.session['user_id']
        user = User.objects.get(user_id=user_id)
        blog_articles = user.blogarticle_set.all()
    else:
        return HttpResponseRedirect('/login/')

    return_info = {'user_id': user_id, 'user': user, 'blog_articles': blog_articles}
    html = get_template('users-window/my-blog-article.html').render(return_info)
    return HttpResponse(html)

# 用户的关注内容的显示方法
def my_attentions(request):
    if 'user_id' in request.session:
        user_id = request.session['user_id']
    else:
        return HttpResponseRedirect('/login/')

    return_info = {'user_id': user_id}
    html = get_template('users-window/my-attentions.html').render(return_info)
    return HttpResponse(html)

# 用户的收藏内容的显示方法
def my_collections(request):
    if 'user_id' in request.session:
        user_id = request.session['user_id']
    else:
        return HttpResponseRedirect('/login/')
    return_info = {'user_id': user_id}
    html = get_template('users-window/my-collections.html').render(return_info)
    return HttpResponse(html)

# 用户的粉丝的显示方法
def my_fans(request):
    if 'user_id' in request.session:
        user_id = request.session['user_id']
    else:
        return HttpResponseRedirect('/login/')
    return_info = {'user_id': user_id}
    html = get_template('users-window/my-fans.html').render(return_info)
    return HttpResponse(html)

# 查重方法，调用了引擎中的SimilarityJudge
# error为True时为异常，similarity为相似度数值，pass为是否被系统认为符合原创
def check_blog_article(content):
    print('接收到文章具体内容content：', content)
    content = content.replace("\n", "")
    similarity = SimilarityJudge().operation(content, 0.9)
    print('相似度为：', similarity)
    if similarity > 0.7:
        return {'error': False, 'similarity': similarity, 'pass': False}
    elif (similarity <= 0.7) and (similarity >= 0):
        return {'error': False, 'similarity': similarity, 'pass': True}
    else:
        return {'error': True, 'similarity': similarity, 'pass': False}

# 用户登录后的博客文章创作页面的显示方法
@csrf_exempt
def write_blog_article(request):
    if 'user_id' in request.session:
        user_id = request.session['user_id']
        article_form = BlogArticleForm()
        if request.method == 'POST':
            print("博客文章提交了,方式为POST。")

            article_form = BlogArticleForm(request.POST)
            if article_form.is_valid():

                cover_img_html = article_form.data.get('cover_img')
                cover_img = re.findall('<img src="(.*?)"', cover_img_html, re.S)
                print('获取到的封面图路径：', cover_img)

                article_html = article_form.data.get('article_html')
                print('博客文章HTML代码：', article_html)

                # 查重反馈信息
                message = check_blog_article(article_html)

                # video_amount可以用来标记是否有视频存在，还可以标记有多少个视频
                video_amount = 0
                if '<embed' in article_html:
                    # 检查到有视频输入
                    urls = re.findall('<embed src="/static/media/upload/(.*?)"', article_html)
                    print('博客文章中有视频，视频文件为：', urls)

                    for url in urls:
                        if os.path.exists('./static/media/upload/' + url):
                            print('视频文件存在')
                            video_amount = video_amount + 1
                        else:
                            print('视频文件不存在，继续执行可能会出错')

                # 从modelform获取数据对象并保存数据对象到数据库
                article_form.instance.author = User.objects.get(user_id=user_id)
                article_form.instance.article_content = '暂时为空'
                article_form.instance.video_amount = video_amount
                article_form.instance.cover_img = cover_img[0]
                title = article_form.save()

                id = article_form.instance.id
                print('通过article_form获取到对应博客文章的id：', id)

                if video_amount > 0:
                    embed_labels_attr = iter(re.findall('<embed src="/static/media/upload/(.*?)/>', article_html, re.S))
                    for i in range(0, video_amount):
                        article_html = re.sub(pattern='<embed src="/static/media/upload/.*?/>', repl='<iframe src="/static/media/upload/%s></iframe>' % next(embed_labels_attr), string=article_html)
                    BlogArticle.objects.filter(id=id).update(article_html=article_html)
                return_info = {'user_id': user_id, 'article_form': article_form, 'message': message}
                html = get_template('users-window/jump-page.html').render(return_info, request)
                return HttpResponse(html)
        return_info = {'user_id': user_id, 'article_form': article_form}
        html = get_template('users-window/write-blog-article.html').render(return_info)
        return HttpResponse(html)
    else:
        return HttpResponseRedirect('/login/')

# 用户登录后用于展示用户个人文章具体内容的方法
def show_my_blog_article_content(request, article_id):
    if 'user_id' in request.session:
        user_id = request.session['user_id']
        blog_article = BlogArticle.objects.get(id=int(article_id))
    else:
        return HttpResponseRedirect('/login/')
    return_info = {'user_id': user_id, 'blog_article': blog_article}
    html = get_template('users-window/my-blog-article-page.html').render(return_info)
    return HttpResponse(html)

# 用户登录后才能删除用户个人文章的显示方法
def blog_article_delete(request, article_id):
    # 删除封面图
    cover_img = str(BlogArticle.objects.get(id=int(article_id)).cover_img)
    if os.path.exists(cover_img):
        os.remove(cover_img)
        print('成功删除路径为', cover_img, '封面图')
    else:
        print('文件不存在，不需要删除。')
    BlogArticle.objects.filter(id=int(article_id)).delete()
    return HttpResponseRedirect('/my-blog-articles/')

# 用户登录后的个人主页的显示方法
def user_homepage(request):
    if 'user_id' in request.session:
        user_id = request.session['user_id']
    else:
        return HttpResponseRedirect('/login/')
    return_info = {'user_id': user_id}
    html = get_template('users-window/user-homepage.html').render(return_info)
    return HttpResponse(html)

# 用户的登录界面的方法
@csrf_exempt
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
                request.session['user_id'] = u.user_id
                return HttpResponseRedirect('/user-information/')
            elif login_user_form.data.get('user_id') == u.user_id and login_user_form.data.get('password') != u.password:
                feedback_message = '密码不对哦大哥'
                break
            else:
                feedback_message = '您还没注册吧？点击下方链接注册一下？或者检查一下您的账号是否写对哦'

    return_info = {'user': user, 'feedback_message': feedback_message}
    html = get_template('users-window/login.html').render(return_info)
    return HttpResponse(html)

# 用户账户注册界面的显示方法
@csrf_exempt
def register(request):
    request.session['user_id'] = None
    register_user = UserRegisterForm()
    if request.method == 'POST':
        register_user = UserRegisterForm(request.POST)
        if register_user.is_valid():
            print(register_user.data)
            register_user.save()
            return HttpResponseRedirect('/login/')
    return_info = {'register_user': register_user}
    html = get_template('users-window/register.html').render(return_info)
    return HttpResponse(html)

def forget_password(request):
    request.session['user_id'] = None
    return_info = {}
    html = get_template('users-window/forget-password.html').render(return_info)
    return HttpResponse(html)

# 请求上墙的方法
def request_on_wall(request, article_id):
    if 'user_id' in request.session:
        user_id = request.session['user_id']
        user = User.objects.get(user_id=user_id)
        blog_articles = user.blogarticle_set.all()

        need_on_wall_article = BlogArticle.objects.get(id=article_id)
        on_walls = OnWall.objects.all()
        for item in on_walls:
            if item.article.id == need_on_wall_article.id:
                on_wall_item = item
                if on_wall_item.examine is True:
                    if on_wall_item.pass_or_not is False:
                        message = "该文章审核不通过，不用再申请了。"
                    else:
                        message = "该文章已经审核通过，您可以在BEE主页的墙上查看。"
                else:
                    message = "该文章已经请求过了，请等待管理员审核。"
                return_info = {'user_id': user_id, 'blog_articles': blog_articles, 'message': message}
                html = get_template('users-window/my-blog-article.html').render(return_info)
                return HttpResponse(html)
        OnWall.objects.create(article=need_on_wall_article)
        message = "提交申请成功，请耐心等待管理员审核。"

        return_info = {'user_id': user_id, 'blog_articles': blog_articles, 'message': message}
        html = get_template('users-window/my-blog-article.html').render(return_info)
        return HttpResponse(html)
    else:
        return HttpResponseRedirect('/login/')




# ######################################################################################################################

# 后台用户管理界面的显示方法
def manage(request):
    need_examine_articles = OnWall.objects.filter(examine=False)
    recommended_request = len(need_examine_articles)

    return_info = {'recommended_request': recommended_request}
    html = get_template('manage-window/index.html').render(return_info)
    return HttpResponse(html)

# 审核上墙请求方法
def examine_on_wall(request):
    recommended_request = len(OnWall.objects.filter(examine=False))

    need_examine = OnWall.objects.filter(examine=False)
    already_examine = OnWall.objects.filter(examine=True)

    return_info = {'need_examine': need_examine, 'already_examine': already_examine, 'recommended_request': recommended_request}
    html = get_template('manage-window/examine-on-wall.html').render(return_info)
    return HttpResponse(html)

# 上墙请求通过审核
def accept_on_wall(request, on_wall_id):
    OnWall.objects.filter(id=on_wall_id).update(examine=True, pass_or_not=True)
    return HttpResponseRedirect('/manage/examine-on-wall/')

def refuse_on_wall(request, on_wall_id):
    OnWall.objects.filter(id=on_wall_id).update(examine=True, pass_or_not=False)
    return HttpResponseRedirect('/manage/examine-on-wall/')

# 后台用户管理的文章分类设计页面的显示方法
def article_sort_design(request):
    recommended_request = len(OnWall.objects.filter(examine=False))

    industry_form = IndustryForm()
    if request.method == 'POST':
        industry_form = IndustryForm(request.POST)
        if industry_form.is_valid():
            industry_form.save()
            return HttpResponseRedirect('/manage/article-sort-design/')
    industry_dict = get_industry_dict()

    return_info = {'recommended_request': recommended_request, 'industry_form': industry_form, 'industry_dict': industry_dict}
    html = get_template('manage-window/article-sort-design.html').render(return_info)
    return HttpResponse(html)

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
    recommended_request = len(OnWall.objects.filter(examine=False))

    return_info = {'recommended_request': recommended_request}
    html = get_template('manage-window/crawl.html').render(return_info)
    return HttpResponse(html)

def crawl_wechat_accounts(request):

    recommended_request = len(OnWall.objects.filter(examine=False))

    wechat_accounts = WechatAccount.objects.all()
    wechat_account_info = None

    if request.method == 'POST':
        wechat_id_dict = request.POST
        print('接收到前端的原始数据：', wechat_id_dict)
        # 以逗号为分割符分割该字符串
        wechat_ids = str(wechat_id_dict['wechat-account-id']).split(',')
        if wechat_ids is not None:
            print('分割后的数据列表：', wechat_ids)

            wechat_account_info = AccountSpider(wechat_ids).get_account_infos()
            print('爬取成功的公众号为：', wechat_account_info)

    return_info = {'recommended_request': recommended_request, 'wechat_accounts':wechat_accounts, 'wechat_account_info':wechat_account_info}
    html = get_template('manage-window/crawl-wechat-accounts.html').render(return_info)
    return HttpResponse(html)
    # return render(request, 'manage-window/crawl-wechat-accounts.html',return_info )

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
    recommended_request = len(OnWall.objects.filter(examine=False))

    accounts = WechatAccount.objects.all()
    message = None
    if request.method == 'POST':
        crawl_accounts = request.POST.getlist('selected_accounts')
        print('接收到要爬取的公众号列表：', crawl_accounts)
        ArticleSpider(crawl_accounts).get_infos()
        message = '爬取完毕，请刷新网页'
    if 'wechat_id' in request.session:
        wechat_id = request.session['wechat_id']
        print('接收到session：wechat_id:', wechat_id)
        if wechat_id is not None:
            wechat_ids = []
            wechat_ids.append(wechat_id)
            ArticleSpider(wechat_ids).get_infos()
            request.session['wechat_id'] = None
    else:
        print('仅打开了爬文章页面。')

    wechat_articles = WeChatArticle.objects.all()

    return_info = {'recommended_request': recommended_request, 'accounts': accounts, 'wechat_articles': wechat_articles, 'message':message}
    html = get_template('manage-window/crawl-wechat-articles.html').render(return_info)
    return HttpResponse(html)

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
    recommended_request = len(OnWall.objects.filter(examine=False))

    wechat_articles = WeChatArticle.objects.all()
    return_info = {'recommended_request': recommended_request, 'wechat_articles':wechat_articles}
    html = get_template('manage-window/show-wechat-articles.html').render(return_info)
    return HttpResponse(html)

def manage_carousel(request):
    recommended_request = len(OnWall.objects.filter(examine=False))

    current_carousels = Carousel.objects.all().order_by('number')
    wechat_articles = WeChatArticle.objects.all()

    return_info = {'recommended_request': recommended_request, 'wechat_articles': wechat_articles, 'current_carousels':current_carousels}
    html = get_template('manage-window/manage-carousel.html').render(return_info)
    return HttpResponse(html)

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
