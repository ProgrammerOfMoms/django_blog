from django.core import paginator
from django.http.response import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views.generic import ListView
from .models import Post


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog_service/post/list.html'


def post_detail(request, year: int, month: int, day: int, post: str) -> HttpResponse:
    """Рендеринг страницы поста"""

    post = get_object_or_404(Post,
                             slug=post,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    return render(request, 'blog_service/post/detail.html', {'post': post})
