from django.db import models

# 文章所属行业和子行业的类
from django.utils import timezone


class Industry(models.Model):
    # 行业名称，不能为空，其对应的子行业可以为空
    industry_name = models.CharField(max_length=10)
    # 子行业名称
    sub_industry_name = models.CharField(max_length=10, null=True, blank=True, unique=True)

    def __str__(self):
        return self.sub_industry_name

# 用户类
class User(models.Model):
    # 用户账号ID就是邮箱，不是Django自创建的id
    user_id = models.EmailField(unique=True)
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

class WeChatArticle(models.Model):
    class Meta:
        # 自定义生成的数据库表名,如果不这样用，系统会默认生成app_wechatarticle的
        db_table = 'wechat_article'
        unique_together = ('publish_date', 'article_title',)

    # 文章id在Django的models中是自动生成的，所以就不写上了
    # 文章发表时间
    publish_date = models.CharField(max_length=20)
    # 文章标题
    article_title = models.CharField(max_length=100)
    # 文章所属公众号名称
    wechat_id = models.CharField(max_length=20)
    # 文章链接，目前暂时是临时的
    article_url = models.TextField()
    # 文章封面图片链接，一个
    cover_img = models.TextField()
    # 文章正文内容
    article_content = models.TextField()
    # 文章图片链接，目前只有一个
    article_img = models.TextField()
    # 文章HTML代码
    article_html = models.TextField()

    def __str__(self):
        return self.article_title

# 博客文章类
class BlogArticle(models.Model):
    class Meta:
        ordering = ('-publish_date',)
    # 标题
    article_title = models.CharField(max_length=100, unique=True)
    # 文章内容
    article_content = models.TextField(null=False)
    # 发表时间
    publish_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.article_title


