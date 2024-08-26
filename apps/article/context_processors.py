from apps.article.models import Category, Tag


def category_list(request):
    category = Category.objects.all()
    tags = Tag.objects.all()
    return {"categories": category, "tags": tags}
