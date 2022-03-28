from django.contrib import admin
from .models import News, Comment, Vote
# Register your models here.

admin.site.register(News)
admin.site.register(Comment)
admin.site.register(Vote)

