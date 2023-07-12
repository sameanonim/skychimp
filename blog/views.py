from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView

from blog.forms import BlogForm
from blog.models import Blog
from blog.services import cache_blog


class RecordListView(ListView):
    model = Blog
    queryset = Blog.objects.filter(published_on=True)

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['blog'] = cache_blog()
        return context_data


class RecordCreateView(LoginRequiredMixin, CreateView):
    model = Blog
    form_class = BlogForm
    success_url = reverse_lazy('blog:record_list')


class RecordUpdateView(LoginRequiredMixin, UpdateView):
    model = Blog
    form_class = BlogForm
    success_url = reverse_lazy('blog:record_list')

    def get_success_url(self):
        return self.object.get_absolute_url()


class RecordDetailView(LoginRequiredMixin, DetailView):
    model = Blog

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        obj.views += 1
        obj.save()
        return obj


class RecordDeleteView(LoginRequiredMixin, DeleteView):
    model = Blog
    success_url = reverse_lazy('blog:record_list')


@permission_required('blog.set_published_blog')
def toggle_activity(request, slug):
    record_item = get_object_or_404(Blog, slug=slug)
    record_item.toggle_published()
    return redirect(reverse('blog:record_detail', args=[record_item.slug]))
