from django import forms

from app.models import *


class UserRegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = "__all__"
        widgets = {
            'user_id': forms.TextInput(attrs={'class': "form-control", 'placeholder': "账号"}),
            'name': forms.TextInput(attrs={'class': "form-control", 'placeholder': "昵称"}),
            'password': forms.PasswordInput(attrs={'class': "form-control", 'placeholder': "密码"}),
            'sex': forms.Select(attrs={'class': "form-control"}),
        }
        error_messages = {
            'user_id': {
                'required': '请使用邮箱注册',
            }
        }
    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        self.fields['user_id'].label = ''
        self.fields['password'].label = ''
        self.fields['name'].label = ''
        self.fields['sex'].label = '性别'
        self.fields['birth_date'].label = '生日'
        # self.fields['head_portrait'].label = '上传头像'


class UserLoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['user_id', 'password']
        widgets = {
            'user_id': forms.TextInput(attrs={'class': "form-control", 'placeholder': "账号"}),
            'password': forms.PasswordInput(attrs={'class': "form-control", 'placeholder': "密码"}),
        }
        error_messages = {
            'user_id': {
                'required': '请使用邮箱登录',
            }
        }
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        self.fields['user_id'].label = ''
        self.fields['password'].label = ''


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['user_id'].label = '账号'
        self.fields['name'].label = '昵称'
        self.fields['sex'].label = '性别'
        self.fields['birth_date'].label = '生日'

class BlogArticleForm(forms.ModelForm):
    class Meta:
        model = BlogArticle
        fields = ['cover_img', 'article_title', 'article_html']
        widgets = {
            'cover_img': forms.FileInput(attrs={'class': "center-block"}),
            'article_title': forms.TextInput(attrs={'class': "form-control", 'placeholder': "请输入文章大标题"}),
            'article_html': forms.TextInput(attrs={'class': "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super(BlogArticleForm, self).__init__(*args, **kwargs)
        self.fields['article_title'].label = '文章标题'
        self.fields['article_html'].label = '文章内容'
        self.fields['cover_img'].label = '请添加文章封面图'


class WeChatArticleForm(forms.ModelForm):
    class Meta:
        model = WeChatArticle
        fields = '__all__'


class IndustryForm(forms.ModelForm):
    class Meta:
        model = Industry
        fields = '__all__'
        widgets = {
            'industry_name': forms.TextInput(attrs={'placeholder': "行业领域"}),
        }

    def __init__(self, *args, **kwargs):
        super(IndustryForm, self).__init__(*args, **kwargs)
        self.fields['industry_name'].label = '领域'

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'
        widgets = {
            'category_name': forms.TextInput(attrs={'placeholder': "分类名称"}),
        }

    def __init__(self, *args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)
        self.fields['category_name'].label = '分类'

class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = '__all__'
        widgets = {
            'tag_name': forms.TextInput(attrs={'placeholder': "标签名称"}),
        }

    def __init__(self, *args, **kwargs):
        super(TagForm, self).__init__(*args, **kwargs)
        self.fields['tag_name'].label = '标签'



