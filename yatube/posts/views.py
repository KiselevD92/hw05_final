from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.cache import cache_page

from .forms import PostForm, CommentForm
from .models import Group, Post, User, Follow
from core.context_processors.paginator import paginator_page


@cache_page(20, key_prefix='index_page')
def index(request):
    post_list = Post.objects.select_related('author', 'group')
    page_obj = paginator_page(request, post_list)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    post_list = group.posts.select_related('author', 'group')
    page_obj = paginator_page(request, post_list)
    context = {
        'page_obj': page_obj,
        'group': group,
    }
    return render(request, 'posts/group_list.html', context)


def profile(request, username):
    author = get_object_or_404(User, username=username)
    post_list = author.posts.select_related("group", "author")
    count_all_posts = author.posts.count()
    page_obj = paginator_page(request, post_list)
    following = request.user.is_authenticated and author.following.exists()
    context = {
        'page_obj': page_obj,
        'author': author,
        'count_all_posts': count_all_posts,
        'following': following,
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    unique_post = get_object_or_404(Post, pk=post_id)
    number_of_posts = unique_post.author.posts.count()
    form = CommentForm(request.POST)
    comments = unique_post.comments.filter(post=unique_post)
    context = {
        'unique_post': unique_post,
        'number_of_posts': number_of_posts,
        'form': form,
        'comments': comments,
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
def post_create(request):
    form = PostForm(
        request.POST or None,
        files=request.FILES or None
    )
    if request.method == 'POST':
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect("posts:profile", post.author)
    return render(request, 'posts/post_create.html', {'form': form})


@login_required
def post_edit(request, post_id):
    post_set = get_object_or_404(Post, id=post_id)
    is_edit = True
    if request.user != post_set.author:
        return redirect("posts:post_detail", post_id)
    form = PostForm(
        request.POST or None,
        files=request.FILES or None,
        instance=post_set
    )
    if form.is_valid():
        form.save()
        return redirect("posts:post_detail", post_id)
    context = {
        'form': form,
        'is_edit': is_edit,
        'post': post_set,
    }
    return render(request, 'posts/post_create.html', context)


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect('posts:post_detail', post_id=post_id)


@login_required
def follow_index(request):
    follower = Post.objects.filter(author__following__user=request.user)
    page_obj = paginator_page(request, follower)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'posts/follow.html', context)


@login_required
def profile_follow(request, username):
    author = get_object_or_404(User, username=username)
    if author != request.user:
        Follow.objects.get_or_create(user=request.user, author=author)
    return redirect('posts:follow_index')


@login_required
def profile_unfollow(request, username):
    author = get_object_or_404(User, username=username)
    Follow.objects.filter(user=request.user, author=author).delete()
    return redirect('posts:follow_index')
