from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from .forms import PostForm
from .models import Post, Group, User


POSTS_ON_PAGE = 10


def index(request):
    """Функция-обработчик главной страницы."""
    template = 'posts/index.html'
    title = 'Это главная страница проекта Yatube'
    post_list = Post.objects.all()
    paginator = Paginator(post_list, POSTS_ON_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'title': title,
        'page_obj': page_obj,
    }
    return render(request, template, context)


def group_post(request, slug):
    """Функция-обработчик страницы запрощенной группы."""
    group = get_object_or_404(Group, slug=slug)
    group_post_list = Post.objects.filter(group=group)
    paginator = Paginator(group_post_list, POSTS_ON_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'group': group,
        'page_obj': page_obj,
    }
    return render(request, 'posts/group_list.html', context)


def profile(request, username):
    """Здесь код запроса к модели и создание словаря контекста."""
    author = get_object_or_404(User, username=username)
    profile_post_list = Post.objects.filter(author_id=author.id)
    paginator = Paginator(profile_post_list, POSTS_ON_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    count = paginator.count
    context = {
        'author': author,
        'count': count,
        'page_obj': page_obj,
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    """Здесь код запроса к модели и создание словаря контекста."""
    post = get_object_or_404(Post, id=post_id)
    title = str(post.text)[:30]
    count = Post.objects.filter(author_id=post.author_id).count()
    context = {
        'title': title,
        'post': post,
        'count': count,
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
def post_create(request):
    form = PostForm(request.POST or None)
    if form.is_valid():
        new_post = form.save(commit=False)
        new_post.author = request.user
        new_post.save()
        return redirect('posts:profile', username=new_post.author)
    return render(request, 'posts/create_post.html', {'form': form})


@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.author.id != request.user.id:
        return redirect('posts:post_detail', post_id=post_id)
    form = PostForm(request.POST or None, instance=post)
    context = {'form': form, 'is_edit': True, 'post_id': post_id}
    # понял, что проверка типа запроса не обязательна, т.к. если валидна,
    # значит и был запрос пост, но пока хочу оставить, чтобы потом вспомнить
    # эту логику
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('posts:post_detail', post_id=post_id)
        return render(request, 'posts/create_post.html', context)
    return render(request, 'posts/create_post.html', context)
