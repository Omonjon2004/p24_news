from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.decorators.cache import cache_page

from apps.article.forms import SearchForm
from apps.article.models import Article, Category, Tag


class HomeView(View):

    def get(self, request):
        articles = Article.published.order_by('-published_at')
        first = articles[0]
        articles = articles[1:]
        tags = Tag.objects.all()
        context = {
            "article": first,
            "articles": articles,
            "tags": tags
        }
        return render(request, "article/index.html", context=context)

    def post(self, request):
        search = request.POST.get('search')
        articles = Article.objects.filter(Q(title__icontains=search) | Q(category__name=search))
        if articles:
            first = articles[0]
            articles = articles[1:]
            tags = Tag.objects.all()
            context = {
                "article": first,
                "articles": articles,
                "tags": tags,
                "search": search
            }
            return render(request, "article/index.html", context=context)

        else:
            return HttpResponse(f"with {search} articles not found ")


class CategoryView(View):
    def get(self, request, pk):
        # category =Category.objects.get(id=pk)
        # articles = Article.objects.filter(category=category)
        articles = Article.objects.filter(category__id=pk)
        context = {
            "articles": articles,
            # "tags": tags
        }
        return render(request, "article/page.html", context=context)


class ArticleDetialView(View):
    def get(self, request, slug):
        article = get_object_or_404(Article, slug=slug)
        return render(request, "article/article.html", {"article": article})
