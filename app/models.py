from django.db import models
import datetime

# 用户类
class User(models.Model):
    # 用户账号ID就是邮箱，不是Django自创建的id
    user_id = models.EmailField(unique=True, null=False)
    # 姓名，昵称
    name = models.CharField(max_length=20, unique=True)
    # 密码
    password = models.CharField(max_length=20)
    # 性别
    SEX = (
        ('man', '男'), ('woman', '女'), ('other', '其他'),
    )
    sex = models.CharField(max_length=6, choices=SEX, default=SEX[0][1:])
    # 生日
    birth_date = models.DateField(blank=True, null=True)
    # 头像
    # head_portrait = models.ImageField(upload_to='user_head_portrait/%Y/%m/%d')

    def __str__(self):
        return self.name


# 公众号类
class WechatAccount(models.Model):
    class Meta:
        # 自定义生成的数据库表名,如果不这样用，系统会默认生成app_wechataccount的
        db_table = 'wechat_account'
        unique_together = ('wechat_id',)

    # 公众号微信号，主键
    wechat_id = models.CharField(max_length=50, primary_key=True, null=False, blank=False)
    # 公众号名称
    wechat_name = models.CharField(max_length=50)
    # 公众号头像图片路径
    head_portrait = models.CharField(max_length=100)
    # 公众号二维码图片路径
    qr_code = models.CharField(max_length=100)

    def __str__(self):
        return u'公众号id：%s  |  公众号名称：%s ' % (self.wechat_id, self.wechat_name)


class WeChatArticle(models.Model):
    class Meta:
        # 自定义生成的数据库表名,如果不这样用，系统会默认生成app_wechatarticle的
        db_table = 'wechat_article'
        unique_together = ('publish_date', 'article_title',)
        ordering = ('-publish_date',)

    # 文章id在Django的models中是自动生成的，所以就不写上了

    # 文章发表时间
    publish_date = models.CharField(max_length=20)
    # 文章标题
    article_title = models.CharField(max_length=100)
    # 文章所属公众号微信号，在经过设置为外键后，在数据库中的属性字段名wechat变更为wechat_id
    wechat = models.ForeignKey(WechatAccount, on_delete=models.CASCADE, null=False)
    # 文章链接，目前暂时是临时的
    article_url = models.TextField()
    # 文章封面图片链接，一个
    cover_img = models.TextField()
    # 文章正文内容
    article_content = models.TextField()
    # 文章HTML代码
    article_html = models.TextField()
    # 文章图片数量
    img_amount = models.IntegerField(default="0")
    # 文章文字数量
    word_amount = models.IntegerField(default="0")
    # 文章视频数量
    video_amount = models.IntegerField(default="0")
    # 文章音频数量
    audio_amount = models.IntegerField(default="0")


    def __str__(self):
        return self.article_title

# 文章所属行业的类
class Industry(models.Model):
    # 行业名称
    industry_name = models.CharField(max_length=30)

    def __str__(self):
        return self.industry_name

# 文章分类，从属于行业类
class Category(models.Model):
    category_name = models.CharField(max_length=30)
    industry = models.ForeignKey(Industry, on_delete=models.CASCADE, null=False)

    def __str__(self):
        return self.category_name

# 标签
class Tag(models.Model):
    tag_name = models.CharField(max_length=30)

    def __str__(self):
        return self.tag_name

# 博客文章类
class BlogArticle(models.Model):
    class Meta:
        ordering = ('-publish_time',)

    # 标题
    article_title = models.CharField(max_length=100)
    # 文章内容
    article_content = models.TextField(null=False)
    # 文章分类
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, blank=True, null=True)
    # 标签
    tags = models.ManyToManyField(Tag, blank=True)
    # 发布时间
    publish_time = models.DateTimeField(auto_now_add=True)
    # 修改时间
    modified_time = models.DateTimeField(auto_now=True)
    # 作者
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    # 文章封面图片链接，一个
    cover_img = models.ImageField(upload_to='static/cover_imgs/%Y/%m/%d/', blank=True, null=True)
    # 文章HTML代码
    article_html = models.TextField()
    # 文章图片数量
    img_amount = models.IntegerField(default=0)
    # 文章文字数量
    word_amount = models.IntegerField(default=0)
    # 文章视频数量
    video_amount = models.IntegerField(default=0)
    # 文章音频数量
    audio_amount = models.IntegerField(default=0)
    # 阅读量
    browsed_times = models.PositiveIntegerField(default=0)
    # 推荐位
    recommend = models.IntegerField(default=0)

    def __str__(self):
        return self.article_title

# 轮播图
class Carousel(models.Model):
    # 轮播图片的链接，记得在后台管理时选择对应的微信文章封面图的路径就行
    img_url = models.TextField()
    # 标题，记得在后台管理时选择对应的微信文章标题就行
    title = models.CharField(max_length=30)
    # 文章的链接
    article_url = models.IntegerField()
    # 图片描述
    alt = models.TextField(null=True, blank=True)
    # 轮播图序号
    number = models.IntegerField(default=0)

    def __str__(self):
        return u'图片链接：%s   文章标题：%s ' % (self.img_url, self.title)

# 友情链接
class Link(models.Model):
    link_name = models.CharField(max_length=20)
    link_url = models.URLField(max_length=200)

    def __str__(self):
        return self.link_name

class OnWall(models.Model):
    # 请求上墙的文章
    article = models.ForeignKey(BlogArticle, on_delete=models.CASCADE, null=False)
    # 标记是否已经检查
    examine = models.BooleanField(default=False)
    # 审批通过或不通过
    pass_or_not = models.BooleanField(default=False)
    # 提交时间
    submit_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s' % self.article_id
