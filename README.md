# Django ORM
## Create
### 기초설정

- shell
```bash
$ python manage.py shell
```
- import model
```python
from articles.models import Article
```

데이터를 저장하는 3가지 방법

1. 첫번째 방법
   - ORM 을 쓰는 이유는? DB 를 조작하는 것을 객체지향 프로그래밍(클래스) 처럼 하기 위해서

```python
>>> article = Article()
>>> article
>>> <Article: Article object (None)>
>>> article.title = 'First Article'
>>> article.content = 'Hello, article?'
>>> article.save()
>>> article
>>> <Article: Article object (1)>
```

2. 두번째 방법
   - 함수에서 keyword 인자 넘기기 방식과 동일

```python
>>> article = Article(title='Second', content='hihi')
>>> article.save()
>>> article
<Article: Article object (2)>
```

3. 세번째 방법
   - Create 를 사용하면 쿼리 셋 객체를 생성하고 저장하는 로직이 한 번의 스텝으로 가능

```python
>>> Article.objects.create(title='third', content='Django! Good')
<Article: Article object (3)>
```

4. 검증

```python
>>> article = Article()
>>> article.title = 'Python is good'
>>> article.full_clean()
Traceback (most recent call last):
  File "<console>", line 1, in <module>
  File "C:\Users\student\Development\Django\Django_orm_crud\venv\lib\site-packages\django\db\models\base.py", line 1203, in full_clean
    raise ValidationError(errors)
django.core.exceptions.ValidationError: {'content': ['이 필드는 빈 칸으로 둘 수 없습니다.']}xxxxxxxxxx >>> article = Article()>>> article.title = 'Python is good'>>> article.full_clean()Traceback (most recent call last):  File "<console>", line 1, in <module>  File "C:\Users\student\Development\Django\Django_orm_crud\venv\lib\site-packages\django\db\models\base.py", line 1203, in full_clean    raise ValidationError(errors)django.core.exceptions.ValidationError: {'content': ['이 필드는 빈 칸으로 둘 수 없습니다.']}article.full_clean()python
```



## Read

### 모든 객체

```python
>>> Article.objects.all()
<QuerySet [<Article: Article object (1)>, <Article: Article object (2)>, <Article: Article object (3)>, <Article: Article object (4)>]>
```

- 객체 표현 변경

```python
class Article(models.Model): # 장고 모델 상속

    def __str__(self):
        return f'{self.id}번 글 - {self.title} : {self.content}'
```

- 객체 표현 변경 후 `exit()` 로 나갔다 다시 들어오기

```python
>>> exit()\
...
(venv)
student@M702 MINGW64 ~/Development/Django/Django_orm_crud (master)
$ python manage.py shell
Python 3.7.4 (tags/v3.7.4:e09359112e, Jul  8 2019, 20:34:20) [MSC v.1916 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license" for more information.
(InteractiveConsole)
>>> from articles.models import Article
>>> Article.objects.all()
<QuerySet [<Article: 1번 글 - First article : Hello, article?>, <Article: 2번 글 - Second article : hihi>, <Article: 3번 글
- third : Django! Good>, <Article: 4번 글 - title : >]>
```

- DB에 저장된 글 중에서 `title`이 `Second`인 글만 가지고 오기

```python
>>> Article.objects.filter(title='Second')
<QuerySet []>
```

- DB 에 저장된 글 중에서 `title` 이 `Second` 인 글 중에서 첫 번째만 가지고 오기

```python
>>> querySet = Article.objects.filter(title='Second')
>>> querySet
<QuerySet [<Article: 5번 글 - Second : content>, <Article: 6번 글 - Second : content>]>
>>> querySet.first
<bound method QuerySet.first of <QuerySet [<Article: 5번 글 - Second : content>, <Article: 6번 글 - Second : content>]>>
>>> querySet.first()
<Article: 5번 글 - Second : content>
-----------------------------------------

>>> Article.objects.filter(title='Second').first()
<Article: 5번 글 - Second : content>

```

- DB 에 저장된 글 중에서 pk 가 1인 글만 가지고 오기

  ### PK 만 ```get()``` 으로 가지고 올 수 있다. ( 고유한 값만)

```python
>>> Article.objects.get(pk=1)
<Article: 1번 글 - First article : Hello, article?>
```

- 오름차순

```python
>>> articles = Article.objects.order_by('pk')
>>> articles
<QuerySet [<Article: 1번 글 - First article : Hello, article?>, <Article: 2번 글 - Second article : hihi>, <Article: 3번 글 - third : Django! Good>, <Article: 4번 글 - title : >, <Article: 5번 글 - Second : content>, <Article: 6번 글 - Second : content>]>
```

- 내림차순

```python
>>> articles = Article.objects.order_by('-pk')
>>> articles
<QuerySet [<Article: 6번 글 - Second : content>, <Article: 5번 글 - Second : content>, <Article: 4번 글 - title : >, <Article: 3번 글 - third : Django! Good>, <Article: 2번 글 - Second article : hihi>, <Article: 1번 글 - First article : Hello, article?>]>
```

- 인덱스 접근 가능

```python
>>> article = articles[2]
>>> article
<Article: 4번 글 - title : >
>>> articles = Article.objects.all()[1:3]
>>> articles
<QuerySet [<Article: 2번 글 - Second article : hihi>, <Article: 3번 글 - third : Django! Good>]>
```

- LIKE - 문자열을 포함하고 있는 값을 가지고 옴

  django ORM 은 이름(`title`)과 필터(`filter`)를 더블 언더스코어로 구분

  ```python
  >>> article = Article.objects.filter(title__contains='Sec')
  >>> article
  <QuerySet [<Article: 2번 글 - Second article : hihi>, <Article: 5번 글 - Second : content>, <Article: 6번 글 - Second : content>]>
  ```

- startswith

```python
>>> articles = Article.objects.filter(title__startswith='first')
>>> articles
<QuerySet [<Article: 1번 글 - First article : Hello, article?>]>
```

- endswith

```python
>>> articles = Article.objects.filter(content__endswith='Good')
>>> articles
<QuerySet [<Article: 3번 글 - third : Django! Good>]>
```

## Delete

article 인스턴스 호출 후 `.delete()` 함수 실행

```python
>>> article = Article.objects.get(pk=2)
>>> article.delete()
(1, {'articles.Article': 1})
```

## Update

article 인스턴스 호출 후 값 변경하여 `save()` 함수 실행

```python
>>> article = Article.objects.get(pk=4)
>>> article.content
''
>>> article.content = 'new content'
>>> article.save()
```

```bash
$ pip install django-extensions
```

```python
settings.py 에 등록
INSTALLED_APPS = [
	django_extensions,
	]
```

```python
$ python manage.py shell_plus
```

