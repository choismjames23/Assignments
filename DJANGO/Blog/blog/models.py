from io import BytesIO
from pathlib import Path
from PIL import Image
from django.db import models
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.urls import reverse

from utils.models import TimestampModel

User = get_user_model()

# TimestampModel 을 상속받는다. -> 여기에는 생성일자, 수정일자가 기본적으로 포함됨
class Blog(TimestampModel):
    CATEGORY_CHOICES = (
        ('free', '자유'),
        ('travel', '여행'),
        ('cat', '고양이'),
        ('dog', '강아지'),
    )
    category = models.CharField('카테고리', max_length=10, choices=CATEGORY_CHOICES, default='free')
    title = models.CharField('제목', max_length=100)
    content = models.TextField('본문')

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    #models.CASCADE => 유저 삭제 시 같이 삭제
    #models.PROTECT => 삭제가 불가능함 (유저를 삭제하려고 할 떄 블로그가 있으면 유저 삭제가 불가능)
    #models.SET_NULL => 유저 삭제 시 블로그의 author가 NULL이 됨

    # null -> db에 빈값이 들어갈 수 있다, blank -> form에서 받을 때 빈값이어도 된다
    image = models.ImageField('이미지', null=True, blank=True, upload_to='blog/%Y/%m/%d')
    thumbnail = models.ImageField('썸네일', null=True, blank=True, upload_to='blog/%Y/%m/%d/thumbnail')

    def __str__(self):
        return f'[{self.get_category_display()}] {self.title[:10]}'

    def get_absolute_url(self):
        return reverse(viewname='blog:detail', kwargs={'blog_pk': self.pk})

    def get_thumbnail_image_url(self):
        if self.thumbnail:
            return self.thumbnail.url
        elif self.image:
            return self.image.url
        else:
            return None

    def save(self, *args, **kwargs):
        if not self.image:
            return super().save(*args, **kwargs)

        image = Image.open(self.image)
        image.thumbnail((300,300))
        image_path = Path(self.image.name)
        thumbnail_name = image_path.stem # /blog/2025/05/16/example.png -> example
                                        # // stem을 사용하면 맨 끝에 파일에서 확장자만 빼고 가져온다
        thumbnail_extension = image_path.suffix.lower() # suffix 를 사용하면 맨 끝에서 확장자를 가져온다. ( .png)
        thumbnail_filename = f'{thumbnail_name}_thumb{thumbnail_extension}' # example_thumb.png

        if thumbnail_extension in ['.jpg', '.jpeg']:
            file_type = 'JPEG'
        elif thumbnail_extension == '.gif':
            file_type = 'GIF'
        elif thumbnail_extension == '.png':
            file_type = 'PNG'
        else:
            return super().save(*args, **kwargs)

        temp_thumb = BytesIO()
        image.save(temp_thumb, file_type)
        temp_thumb.seek(0)

        self.thumbnail.save(thumbnail_filename, temp_thumb, save=False)
        temp_thumb.close()
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = '블로그'
        verbose_name_plural = '블로그 목록'

class Comment(TimestampModel):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    content = models.CharField('본문', max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.blog.title} 댓글'

    class Meta:
        verbose_name = '댓글'
        verbose_name_plural = '댓글 목록'
        ordering = ('-created_at','-id')

