from xml.etree.ElementTree import Comment
from django.shortcuts import render, get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response 
from drf_yasg.utils import swagger_auto_schema
from . import serializers
from .models import News, Vote, Comment
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly
from django.contrib.auth import get_user_model

User=get_user_model()

class NewsCreateListView(generics.GenericAPIView):
    serializer_class = serializers.NewsSerializer
    permission_classes=[IsAuthenticatedOrReadOnly]
    
    @swagger_auto_schema(operation_summary="Listing all news")
    def get(self, request):    
        
        news=News.objects.all()
        serializer = self.serializer_class(instance = news, many = True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(operation_summary="Creating news")
    def post(self, request):
        data = request.data
        
        serializer = self.serializer_class(data=data)
        
        owner=request.user
        
        if serializer.is_valid():
            serializer.save(owner=owner)

            return Response(data = serializer.data, status= status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class NewsDetailView(generics.GenericAPIView):
    serializer_class=serializers.NewsDetailSerializer
    permission_classes=[IsAuthenticatedOrReadOnly]
    
    @swagger_auto_schema(operation_summary="Getting specific news by ID")
    def get(self, request, news_id):
        
        news = get_object_or_404(News, pk=news_id)
        
        serializer = self.serializer_class(instance=news)
        
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(operation_summary="Editing specific news by ID")
    def put(self, request, news_id):
        data=request.data
        
        news = get_object_or_404(News, pk=news_id)

        serializer=self.serializer_class(data=data, instance=news)
        
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(operation_summary="Deleting specific news by ID")
    def delete(self, news_id):
        news = get_object_or_404(News, pk=news_id)
        
        news.delete()
        
        return Response(status= status.HTTP_204_NO_CONTENT)


class UserNewsView(generics.GenericAPIView):
    serializer_class=serializers.NewsDetailSerializer
    
    @swagger_auto_schema(operation_summary="Listing User`s news")
    def get(self, request, user_id):
        user = User.objects.get(pk=user_id)
        
        news = News.objects.all().filter(owner=user)
        
        serializer = self.serializer_class(instance=news, many=True)
        
        return Response(data=serializer.data, status=status.HTTP_200_OK)



class NewsVoteView(generics.GenericAPIView):
    serializer_class=serializers.VoteSerializer
    permission_classes=[IsAuthenticated]
    
    @swagger_auto_schema(operation_summary="Voting or changin editing your vote")
    def post(self, request, news_id):
        
        news = News.objects.get(id=news_id)
        author = request.user
        data = request.data
        
        vote, created = Vote.objects.get_or_create(
            author = author,
            news = news,
        )
        
        vote.value = data['value']
        vote.save()
        news.getVoteCount
        
        serializer = serializers.NewsDetailSerializer(instance=news, many=False)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    
class NewsCommentView(generics.GenericAPIView):
    serializer_class=serializers.VoteSerializer
    permission_classes=[IsAuthenticated]
    
    @swagger_auto_schema(operation_summary="Commenting news")
    def post(self, request, news_id):
        news = News.objects.get(id=news_id)
        author = request.user
        data = request.data
        
        comment = Comment.objects.create(
            author = author,
            news = news,
        )
        
        comment.content = data['content']
        comment.save()
        
        serializer = serializers.NewsDetailSerializer(instance=news, many=False)
        return Response(data=serializer.data, status=status.HTTP_200_OK)