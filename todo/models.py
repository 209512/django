from django.db import models
from django.contrib.auth import get_user_model
from io import BytesIO
from pathlib import Path
from PIL import Image
from django.core.files.base import ContentFile
from django.core.files import File

User = get_user_model()

class Todo(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='todos')
    completed_image = models.ImageField(
        upload_to='todo/completed_images/',
        null=True, blank=True
    )
    thumbnail = models.ImageField(
        upload_to='todo/thumbnails/',
        null=True, blank=True,
        default='todo/thumbnails/default_thumbnail.jpg'
    )

    def save(self, *args, **kwargs):
        # 기존 객체의 이미지 정보를 가져오기 (업데이트 시에만 작동)
        try:
            this = Todo.objects.get(id=self.id)
            if this.completed_image != self.completed_image:
                # 기존 썸네일 파일 삭제
                if this.thumbnail and Path(this.thumbnail.name).name != 'default_thumbnail.jpg':
                    this.thumbnail.delete(save=False)
        except Todo.DoesNotExist:
            pass  # 객체가 새로 생성될 때는 무시

        # completed_image가 있고, 파일이 수정되거나 새로 업로드되었을 때만 썸네일 생성
        if self.completed_image and isinstance(self.completed_image, File):
            img = Image.open(self.completed_image)
            img.thumbnail((200, 200))

            ext = Path(self.completed_image.name).suffix.lower()
            if ext in ['.jpg', '.jpeg']:
                file_type = 'JPEG'
            elif ext == '.png':
                file_type = 'PNG'
            elif ext == '.gif':
                file_type = 'GIF'
            else:
                file_type = 'JPEG'

            temp_thumb = BytesIO()
            img.save(temp_thumb, file_type)
            temp_thumb.seek(0)

            thumb_name = Path(self.completed_image.name).stem + '_thumb' + ext
            self.thumbnail.save(thumb_name, ContentFile(temp_thumb.read()), save=False)
            temp_thumb.close()
        # completed_image가 없으면 썸네일도 기본값으로 설정
        elif not self.completed_image and self.thumbnail:
            self.thumbnail = self._meta.get_field('thumbnail').default

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']

class Comment(models.Model):
    todo = models.ForeignKey(Todo, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    message = models.TextField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user}: {self.message}'

    class Meta:
        ordering = ['created_at'] # 댓글 오래된 순 정렬