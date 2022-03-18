from sys import path_hooks
from unicodedata import name
from django.urls import path
from .views import *

urlpatterns = [
    path('post/post_list', PostListView.as_view(), name='post_list'),
    path('post/post_list/<int:id>', PostDetailView.as_view(), name = 'post_detail'),
    path('post/timeline', PostTimeLineView.as_view(), name = 'timeline'),
    path('post/comment_list', CommentListView.as_view(), name = 'comment_list'),
    path('post/comment_delete/<int:id>', CommentDeleteView.as_view(), name = 'comment_delete'),
    path('post/reaction_list', ReactionListView.as_view(), name = 'reaction_list'),
    path('post/reaction_delete/<int:id>', ReactionDeleteView.as_view(), name = 'reaction_delete')
]
