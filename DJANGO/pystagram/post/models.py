from django.contrib.auth import get_user_model
from django.db import models
from utils.models import TimestampModel

User = get_user_model()

class Post(TimestampModel):
    content = models.TextField('본문')
    user = models.ForeignKey(User, on_delete=models.CASCADE) # user가 삭제되면 post도 같이 삭제

    def __str__(self):
        return f'[{self.user}] post'

    class Meta:
        verbose_name = '포스트'
        verbose_name_plural = '포스트 목록'

class PostImage(TimestampModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images') # post가 삭제되면 이미지도 같이 삭제
    image = models.ImageField(verbose_name='이미지', upload_to='post/%y/%m/%d')

    def __str__(self):
        return f'{self.post} image'

    class Meta:
        verbose_name = '이미지'
        verbose_name_plural = '이미지 목록'


class Tag(TimestampModel):
    tag = models.CharField('태그', max_length=100)
    posts = models.ManyToManyField(Post, related_name='tags')

    def __str__(self):
        return self.tag

class Comment(TimestampModel):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    content = models.CharField('내용', max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.post} | {self.user}'