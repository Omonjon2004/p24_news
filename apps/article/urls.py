from django.urls import path
from django.views.decorators.cache import cache_page

from apps.article.views import HomeView, CategoryView, ArticleDetialView

app_name = 'article'
urlpatterns = [
    path('', cache_page(60 * 15)(HomeView.as_view()), name="home"),
    path('<slug:slug>', ArticleDetialView.as_view(), name="article-detail"),
    path('category/<pk>/', CategoryView.as_view(), name="category")
]
