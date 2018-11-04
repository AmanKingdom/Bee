from django.db import models

# 导航类，用于生成一个
class Navigation(models.Model):
    industry = models.CharField(max_length=10)

    def __str__(self):
        return self.industry
