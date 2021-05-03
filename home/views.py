from django.shortcuts import get_object_or_404, redirect, reverse, render
from django.http import HttpResponseForbidden
from django.urls import reverse_lazy
from django.views.generic import ListView, FormView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q, Count
from django.contrib import messages
from home.forms import CommentForm
from .models import Post, Comment
from django.views import View
from django.http import JsonResponse


def register_validate(request):
    username = request.GET.get('username', None)
    email = request.GET.get('email', None)
    if username:
        is_taken = User.objects.filter(username__exact=username).exists()
        data = {
            'is_invalid': is_taken
        }
        if is_taken:
            data['error_message'] = 'This username already exists'
    elif email:
        is_taken = User.objects.filter(email__exact=email).exists()
        data = {
            'is_invalid': is_taken
        }

        if is_taken:
            data['error_message'] = 'This email already exists'

    return JsonResponse(data)


class PostListView(ListView):
    model = Post
    template_name = 'home/home.html'
    context_object_name = 'posts'
    paginate_by = 3

    def get_queryset(self):
        return Post.objects.filter(is_approved=True).order_by('-date_posted')

    def get_context_data(self, **kwargs):
        context = super(PostListView, self).get_context_data(**kwargs)
        context['most_commented_posts'] = Post.approved.annotate(count=Count('comments')).order_by('-count')[:7]
        return context


class PostSearchView(ListView):
    model = Post
    template_name = 'home/search.html'
    context_object_name = 'posts'
    paginate_by = 3

    def get_queryset(self):
        query = self.request.GET['search']
        if query:
            return Post.approved.filter(Q(title__icontains=query) | Q(content__icontains=query) | Q(author__username__icontains=query)).distinct().order_by('-date_posted')
        return Post.approved.all().order_by('-date_posted')


class PostByAuthorView(ListView):
    model = Post
    template_name = 'home/post_by_author.html'
    context_object_name = 'posts'
    paginate_by = 3

    def get_queryset(self):
        author = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.approved.filter(author=author).order_by('-date_posted')


class PostByDateView(ListView):
    model = Post
    template_name = 'home/post_by_date.html'
    context_object_name = 'posts'
    paginate_by = 3

    def get_queryset(self):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        return Post.approved.filter(date_posted__year=year, date_posted__month=month).order_by('-date_posted')


class PostDetailView(View):
    template_name = 'home/post_detail.html'
    form_class = CommentForm

    def get(self, request, *args, **kwargs):
        form = self.form_class
        post = get_object_or_404(Post, slug=kwargs.get('slug'))
        comments = Comment.objects.filter(post=post)
        return render(request, self.template_name, {'post': post, 'comments': comments, 'form': form})

    def post(self, request, *args, **kwargs):
        user = self.request.user
        if user.is_active:
            form = self.form_class(request.POST)
            post = get_object_or_404(Post, slug=kwargs.get('slug'))
            comments = Comment.objects.filter(post=post)
            if form.is_valid():
                parent = form.cleaned_data.get('parent')
                comment_body = form.cleaned_data.get('comment_body')
                comment = Comment(user=user, post=post, comment_body=comment_body, parent=parent)
                comment.save()
                return redirect(reverse('post-detail', kwargs={'slug': kwargs.get('slug')}))
            else:
                return render(request, self.template_name, {'post': post, 'comments': comments, 'form': form})
        else:
            return redirect('login')


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, View):
    def get(self, *args, **kwargs):
        comment = get_object_or_404(Comment, id=kwargs.get('pk'))
        post_slug = kwargs.get('slug')
        comment.delete()
        messages.success(self.request, 'Your Comment is Deleted Successfully')
        return redirect(reverse('post-detail', kwargs={"slug": post_slug}))

    def test_func(self):
        comment = get_object_or_404(Comment, id=self.kwargs.get('pk'))
        return self.request.user == comment.user or self.request.user.is_staff


class PostCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'slug', 'image', 'content']
    success_message = "Your Post is Created successfully, it will be added to Homepage after approval"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(PostCreateView, self).get_context_data(**kwargs)
        context['page_name'] = "Create Post"
        return context


class PostUpdateView(SuccessMessageMixin, LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'slug', 'image', 'content']
    success_message = "Your Post is Updated successfully, it will be added to Homepage after approval"

    def form_valid(self, form):
        form.instance.is_approved = False
        return super().form_valid(form)

    def test_func(self):  # will return true if current user is post's author or current user is admin
        post = self.get_object()
        return self.request.user == post.author or self.request.user.is_staff

    def get_context_data(self, **kwargs):
        context = super(PostUpdateView, self).get_context_data(**kwargs)

        context['page_name'] = "Update Post"
        if self.object.image:  # Checking if image exists
            context['image'] = self.object.image.url
        else:
            context['image'] = ""
        return context


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, View):

    def get(self, *args, **kwargs):
        post = get_object_or_404(Post, id=kwargs.get('pk'))
        print(post)
        post.delete()
        messages.success(self.request, 'Your Comment is Deleted Successfully')
        return redirect('home')

    def test_func(self):  # will return true if current user is post's author or current user is admin
        post = get_object_or_404(Post, id=self.kwargs.get('pk'))
        print(post)
        return self.request.user == post.author or self.request.user.is_staff
