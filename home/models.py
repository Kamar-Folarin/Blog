from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.utils import timezone
from django.contrib.auth.models import User
from django.shortcuts import reverse


class ApprovedPostManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_approved=True)


class Post(models.Model):
    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    content = models.TextField()
    image = models.ImageField(upload_to='posts/', blank=True)
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    is_approved = models.BooleanField(default=False)  # can only be approved by admin from admin page
    # so all created posts can be checked before being published
    objects = models.Manager()
    approved = ApprovedPostManager()

    def __str__(self):
        return f'{self.title} - Approved : {self.is_approved}'

    def get_absolute_url(self, **kwargs):
        return reverse('post-detail', kwargs={'slug': self.slug})


class Comment(MPTTModel):
    comment_body = models.TextField(blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    date_posted = models.DateTimeField(auto_now_add=True)
    parent = TreeForeignKey('self', null=True, db_index=True, default=None, blank=True, on_delete=models.CASCADE, related_name='children')

    class Meta:
        ordering = ['-date_posted']

    def __str__(self):
        return f'Comment by {self.user} on {self.post}'
