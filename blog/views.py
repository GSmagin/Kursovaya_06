from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib import messages
from django.shortcuts import render, redirect
import transliterate
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.text import slugify
from django.views.decorators.cache import never_cache
from django.views.generic import DetailView, ListView, UpdateView, DeleteView, TemplateView, CreateView
from django.core.exceptions import PermissionDenied
from config.settings import CACHE_ENABLED

from blog.forms import PostForm
from blog.models import BlogMod
from blog.servises import get_blog_from_cache
from blog.utils.mail_newsletter import congratulate_mail_newsletter


class BlogDetailView(DetailView):
    model = BlogMod
    template_name = 'blog/blogpost_detail.html'
    context_object_name = 'blog'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.views_count += 1
        obj.save()
        congratulate_mail_newsletter(obj)
        return obj


class BlogListView(ListView):
    model = BlogMod
    template_name = 'blog/blogpost_list.html'
    context_object_name = 'blog'
    paginate_by = 10

    def get_queryset(self):
        # Проверяем наличие прав у пользователя
        if self.request.user.has_perm('blog.can_publish_post'):
            if CACHE_ENABLED:
                return get_blog_from_cache()
            return BlogMod.objects.all()
        else:
            # Для обычных пользователей используем только опубликованные посты
            if CACHE_ENABLED:
                blog_list = get_blog_from_cache()
                return blog_list.filter(is_published=True)
            return BlogMod.objects.filter(is_published=True)

        # if self.request.user.has_perm('blog.can_publish_post'):
        #     return BlogMod.objects.all()
        # return BlogMod.objects.filter(is_published=True)


class BlogCreateView(CreateView):
    form_class = PostForm
    model = BlogMod
    template_name = 'blog/blogpost_form.html'
    #fields = ["title", "content", "preview_image", "is_published"]
    success_url = reverse_lazy('blog:blogpost_list')

    # def form_valid(self, form):
    #     if form.is_valid():
    #         new_post = form.save(commit=False)
    #         new_post.slug = slugify(new_post.title)
    #         new_post.save()
    #     return super().form_valid(form)

    @method_decorator(never_cache)
    def dispatch(self, *args, **kwargs):
        """Отключение кеша"""
        return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        title = transliterate.slugify(form.cleaned_data['title'])
        if self.model.objects.filter(slug=title).exists():
            form.add_error('title', 'Пост с таким slug уже существует')
            return self.form_invalid(form=form)

        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("blog:blogpost_detail", args=[self.object.pk])


class BlogUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = BlogMod
    form_class = PostForm
    template_name = 'blog/blogpost_form.html'
    context_object_name = 'blog'
    success_url = reverse_lazy('blog:blogpost_detail')
    permission_required = 'blog.can_edit_post'

    # def dispatch(self, request, *args, **kwargs):
    #     user = self.request.user
    #     if (not self.request.user.has_perm('blog.can_publish_post')
    #             and not self.request.user == self.get_object().author
    #             and not user.groups.filter(name='Admin').exists()):
    #         raise PermissionDenied
    #     return super().dispatch(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        post = self.get_object()
        if not (request.user == post.author or request.user.has_perm('blog.can_edit_post')):
            messages.error(request, 'У вас нет прав для редактирования этого поста.')
            return redirect('blog:blogpost_list')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.slug = slugify(new_post.title)
            new_post.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("blog:blogpost_detail", args=[self.object.pk])


class BlogDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = BlogMod
    template_name = 'blog/blogpost_confirm_delete.html'
    success_url = reverse_lazy('blog:blogpost_list')
    permission_required = 'blog.can_edit_post'

    def dispatch(self, request, *args, **kwargs):
        post = self.get_object()
        user = request.user

        # Проверка, является ли пользователь владельцем поста или имеет разрешение на редактирование поста
        if (not self.request.user.has_perm('blog.can_publish_post')
                and not self.request.user == self.get_object().author
                and not user.groups.filter(name='Admin').exists()):
            return redirect('blog:blogpost_list')

        return super().dispatch(request, *args, **kwargs)
