from django.contrib import admin

from .models import *

@admin.register(BlogArticle)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['article_title']
    class Media:
        # 在管理后台的HTML文件中加入js文件, 每一个路径都会追加STATIC_URL/
        js = (
            # '/static/assets/js/kindeditor_source/kindeditor-all-min.js',
            '/static/assets/js/kindeditor_source/kindeditor-all.js',
            '/static/assets/js/kindeditor_source/lang/zh-CN.js',
            '/static/assets/js/kindeditor_source/config.js',
        )

admin.site.register(User)
admin.site.register(Industry)
admin.site.register(WeChatArticle)
admin.site.register(WechatAccount)
admin.site.register(Carousel)
