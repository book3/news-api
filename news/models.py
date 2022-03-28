
from django.db import models
from django.contrib.auth import get_user_model
import uuid

User = get_user_model()

# title, link, creation date, amount of upvotes, author-name
class News(models.Model):
    
    owner=models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    news_link = models.CharField(max_length=200, blank=True, null=True)
    vote_total = models.IntegerField(default=0, null=True, blank=True)
    vote_ratio = models.IntegerField(default=0, null=True, blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-vote_ratio', '-vote_total']
    
    @property
    def getVoteCount(self):
        votes = self.vote_set.all()
        upVotes = votes.filter(value='up').count()
        totalVotes = votes.count()
        ratio = (upVotes / totalVotes) * 100
        self.vote_total = totalVotes
        self.vote_ratio = ratio
        self.save()

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    news = models.ForeignKey(News, on_delete=models.CASCADE)
    content = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)
    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return self.content

class Vote(models.Model):
    VOTE_TYPE = (
        ('up', 'Up Vote'),
        ('down', 'Down Vote'),
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    news = models.ForeignKey(News, on_delete=models.CASCADE)
    value = models.CharField(max_length=200, choices=VOTE_TYPE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = [['author', 'news']]
    
    def __str__(self):
        return self.value