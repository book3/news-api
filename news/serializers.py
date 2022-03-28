from .models import News, Comment, Vote
from rest_framework import serializers
from users.serializers import UserCreationSerializer

class CommentsSerializer(serializers.ModelSerializer):
    content = serializers.CharField()
    class Meta:
        model = Comment
        fields = ['content']


class NewsSerializer(serializers.ModelSerializer):
    author_name = serializers.SerializerMethodField(read_only=True)
    title = serializers.CharField(max_length=200)
    news_link = serializers.CharField(max_length=200)
    
    class Meta:
        model = News
        fields = [
            'author_name',
            'id',
            'title',
            'news_link',
            'vote_ratio',
            'created_at',
            'comments'
        ]
    comments = serializers.SerializerMethodField()
    
    def get_comments(self, obj):
        comment = obj.comment_set.all()
        serializer = CommentsSerializer(comment, many=True)
        return serializer.data
    
    def get_author_name(self, obj):
        name = obj.owner.username
        return name
    
class NewsDetailSerializer(serializers.ModelSerializer):
    
    author_name = serializers.SerializerMethodField(read_only=True)
    news_link = serializers.CharField(max_length=200)
    vote_total = serializers.IntegerField(read_only=True)
    vote_ratio = serializers.IntegerField(read_only=True)
    created_at=serializers.DateTimeField(read_only=True)
    updated_at=serializers.DateTimeField(read_only=True)
    
    class Meta:
        model = News
        fields = [
            'author_name',
            'title',
            'news_link',
            'vote_total',
            'vote_ratio',
            'created_at',
            'updated_at',
            'comments'
            ]
    comments = serializers.SerializerMethodField()
    
    def get_comments(self, obj):
        comment = obj.comment_set.all()
        serializer = CommentsSerializer(comment, many=True)
        return serializer.data
    
    def get_author_name(self, obj):
        name = obj.owner.username
        return name

class VoteSerializer(serializers.ModelSerializer):
    author = UserCreationSerializer(read_only=True)
    news = NewsSerializer(read_only=True)
    value = serializers.CharField(max_length=200)
    class Meta:
        model = Vote
        fields = '__all__'