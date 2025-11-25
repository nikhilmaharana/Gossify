from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Post, Like, Comment
from .forms import PostForm, CommentForm


def home(request):
    """Home page with public feed"""
    # Prefetch likes and comments for performance
    posts_list = Post.objects.select_related('author').prefetch_related('likes', 'comments').all()
    
    paginator = Paginator(posts_list, 10)  # 10 posts per page
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)

    # Add liked_by_user property for each post
    for post in posts:
        post.liked_by_user = post.likes.filter(user=request.user).exists() if request.user.is_authenticated else False

    # Blank comment form for all posts
    comment_form = CommentForm()

    return render(request, 'home.html', {
        'posts': posts,
        'comment_form': comment_form
    })


@login_required
def create_post(request):
    """Create a new post"""
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.anonymous = form.cleaned_data.get('anonymous', False)
            post.save()
            messages.success(request, 'Post created successfully!')
            return redirect('home')
    else:
        form = PostForm()

    return render(request, 'posts/create.html', {'form': form})


@login_required
def edit_post(request, post_id):
    """Edit an existing post"""
    post = get_object_or_404(Post, id=post_id, author=request.user)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.anonymous = form.cleaned_data.get('anonymous', False)
            post.save()
            messages.success(request, 'Post updated successfully!')
            return redirect('user_posts')
    else:
        form = PostForm(instance=post)

    return render(request, 'posts/edit.html', {'form': form, 'post': post})


@login_required
def delete_post(request, post_id):
    """Delete a post"""
    post = get_object_or_404(Post, id=post_id, author=request.user)
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Post deleted successfully!')
        return redirect('user_posts')

    return render(request, 'posts/delete.html', {'post': post})


@login_required
def user_posts(request):
    """Display logged-in user's own posts"""
    posts = Post.objects.filter(author=request.user).prefetch_related('likes', 'comments')
    comment_form = CommentForm()

    return render(request, 'posts/user_posts.html', {
        'posts': posts,
        'comment_form': comment_form
    })


# -------------------------
# Additional Like & Comment Views
# -------------------------

@login_required
def toggle_like(request, post_id):
    """Like or unlike a post"""
    post = get_object_or_404(Post, id=post_id)
    like, created = Like.objects.get_or_create(post=post, user=request.user)
    if not created:
        # If it already exists, unlike it
        like.delete()
    return redirect(request.META.get('HTTP_REFERER', 'home'))


@login_required
def add_comment(request, post_id):
    """Add a comment to a post"""
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
            messages.success(request, 'Comment added successfully!')
    return redirect(request.META.get('HTTP_REFERER', 'home'))
