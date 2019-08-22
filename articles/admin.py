from django.contrib import admin
from .models import Article   # .models <= 현재 디렉토리에 있는 models에서 Article 모듈을 가져오겠다.

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'content', 'created', 'updated_at',)
    # 어떤 필드를 보여줄지 정하는 것



# Register your models here.
# admin.site.register(Article) # admin 사이트에 Article 모델을 등록하겠다. 


