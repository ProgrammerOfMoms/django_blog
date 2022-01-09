from django.http.response import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from django.core.mail import send_mail
from django.conf import settings
from .models import Post
from .forms import EmailPostForm


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


def post_share(request, post_id) -> HttpResponse:
    """Обработчик 'Поделиться постом'"""
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False
    if request.method == "POST":
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f'{cleaned_data["name"]} ({cleaned_data["email"]}) recommends you reading {post.title}'
            message = f'Read "{post.title}" at {post_url}\n\n{cleaned_data["name"]}\'s comments: {cleaned_data["comment"]}'
            send_mail(subject, message, settings.EMAIL_HOST, [cleaned_data["to"]])
            sent=True
    else:
        form = EmailPostForm()
    return render(request, 'blog_service/post/share.html', {'post': post, 'form': form, 'sent': sent})
