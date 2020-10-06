from django.db import models

from django.core.validators import FileExtensionValidator # Validator for image file extensions
from profiles.models import Profile

# Create your models here.
class Post(models.Model):
    content = models.TextField()
    image = models.ImageField(upload_to='posts', validators=[
        FileExtensionValidator([
            'png', 'jpg', 'jpeg',
        ])
    ], blank=True)
    liked = models.ManyToManyField(Profile, blank=True, related_name='likes')

    # post Owner
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='posts')

    # timeTrack
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.content[:20])

    # count number of Likes
    def number_of_likes(self):
        return self.liked.all().count()

    # number of comments
    def number_of_comments(self):
        return self.comment_set.all().count()


    class Meta:
        ordering = ('-created',)


# Comments Model

class Comment(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    body = models.TextField(max_length=500)

    # timeTrack
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.pk)

# Like Model
LIKE_CHOICES= (
    ('LI', 'Like'),
    ('UN-L', 'Unlike')
)

class Like(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    value = models.CharField(max_length=4 ,choices=LIKE_CHOICES)

    # timeTrack
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user} | {self.post} | {self.value}"
