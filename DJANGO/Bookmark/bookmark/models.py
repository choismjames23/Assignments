from django.db import models

# Create your models here.

#Model = DB의 테이블
#Field = DB의 컬럼

class Bookmark(models.Model):
    name = models.CharField('이름', max_length=100)
    url = models.URLField('URL')
    created_at = models.DateTimeField('생성일시',auto_now_add=True)
    updated_at = models.DateTimeField('수정일시',auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'bookmark'
        verbose_name_plural = 'bookmark list'


# makemigrations => migration.py 파일을 만든다
# 실제 DB에 영향 X => 실제 DB에 넣기 위한 정의를 하는 파일을 생성
# migrate => migrations/ 폴더 안에 있는 migration 파일들을 실제 DB에 적용

# makemigrations => git의 커밋 => github에 적용 X => DB에 적용 X, 적용할 파일 생성
# migrate => git의 push => github에 적용 O, 로컬에 있는 커밋 기록 사용 => DB에 적용 O, migrations 파일들을 가지고 적용