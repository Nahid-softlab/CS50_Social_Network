from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    content = models.CharField(max_length=1400)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="creator")
    dateofcontent = models.DateTimeField(auto_now_add=True)
    number_of_likes = models.IntegerField(default=0)

    def __str__(self):
        return f"post {self.id} made by {self.user} on { self.dateofcontent.strftime('%d-%b-%Y %H:%M:%S')}"

class Follow(models.Model):
    mainuser_follow = models.ForeignKey(User, on_delete=models.CASCADE, related_name="mainuser")
    followingUsers = models.ForeignKey(User, on_delete=models.CASCADE, related_name="allusers_of_following_lsit")

    def __str__(self):
        return f" {self.mainuser_follow} is follwing {self.followingUsers}"

class Like(models.Model):
    mainuser_like = models.ForeignKey(User, on_delete=models.CASCADE, related_name="mainuser_like")
    liked_post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="Liked_post_list")

    def __str__(self):
        return f"{self.mainuser_like} likes {self.liked_post}"