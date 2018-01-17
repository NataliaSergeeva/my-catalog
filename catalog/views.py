from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import auth
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.contrib.auth import authenticate, login, logout
from django.template.context_processors import csrf
from .models import Post, Comment
from .forms import PostForm, CommentForm
from django.core.files import File
from django.views import View

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    return render(request, 'catalog/post_list.html', {'posts': posts})

class PostView(View):
    template_name = 'catalog/post_detail.html'
    comment_form = CommentForm

    def get(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        context = {}
        context.update(csrf(request))
        user = auth.get_user(request)
        context['comments'] = post.comments.all()
        context['post'] = post
        if user.is_authenticated:
            context['form'] = self.comment_form

        return render(request, template_name=self.template_name, context=context)

@require_http_methods(["POST"])
def add_comment_to_post(request, pk):

    form = CommentForm(request.POST)
    post = get_object_or_404(Post, pk=pk)

    if form.is_valid():
        comment = Comment()
        comment.post_id = pk
        comment.author = form.cleaned_data['author_name']
        comment.text = form.cleaned_data['comment_area']
        comment.save()

    return redirect('post_detail', pk=post.pk)

@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'catalog/post_edit.html', {'form': form})

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'catalog/post_edit.html', {'form': form})


def contacts(request):
    return render(request, 'catalog/contacts.html')

    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'catalog/add_comment_to_post.html', {'form': form})

@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)

@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('post_detail', pk=comment.post.pk)


@login_required
def post_draft_list(request):
    posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
    return render(request, 'catalog/post_draft_list.html', {'posts': posts})

@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)

@login_required
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')
