from django.http.response import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Count
from taggit.models import Tag
from .models import Post
from .forms import EmailPostForm, CommentForm


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog_service/post/list.html'

    def get_queryset(self):
        if "tag_slug" in self.kwargs:
            tag = get_object_or_404(Tag, slug=self.kwargs["tag_slug"])
            return Post.published.all().filter(tags__in=[tag])
        return super().get_queryset()


def post_detail(request, year: int, month: int, day: int, post: str) -> HttpResponse:
    """Рендеринг страницы поста"""

    post = get_object_or_404(Post,
                             slug=post,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    comments = post.comments.filter(active=True)
    new_comment = None
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
    else:
        comment_form = CommentForm()

    # Похожие статьи
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids)\
                                  .exclude(id=post.id)\
                                  .annotate(same_tags=Count('tags'))\
                                  .order_by('-same_tags', '-publish')
    return render(request, 'blog_service/post/detail.html', {'post': post,
                                                             'comments': comments,
                                                             'new_comment': new_comment,
                                                             'comment_form': comment_form,
                                                             'similar_posts': similar_posts})


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
