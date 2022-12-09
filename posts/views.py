from django.shortcuts import render
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from users.models import UserProfile
from .models import Post
from django.views.generic import ListView, CreateView, UpdateView, DetailView

class UserInfoMixin:

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        req_user = self.request.user
        if req_user.is_authenticated:
            user_profile = get_object_or_404(UserProfile, user=req_user)
            context['user_id'] = user_profile.pk
            context['first_name'] = user_profile.first_name
            context['last_name'] = user_profile.last_name
        return context



# Create your views here.
class PostDetailView(UserInfoMixin, DetailView):
    model = Post
    slug_field = 'id'
    slug_url_kwarg = 'id'


class PostsListView(UserInfoMixin, ListView):
    model = Post
    paginate_by = 5


class PostsCreateView(UserInfoMixin, CreateView):
    model = Post
    success_url = reverse_lazy('posts:posts_list')
    # fields = '__all__'
    fields = ('preview_pic', 'title', 'body')
    template_name_suffix = '_create_form'

    def form_valid(self, form):
        form.instance.author = get_object_or_404(UserProfile, pk=self.request.user.userprofile.id)
        return super().form_valid(form)


class PostsUpdateView(UserInfoMixin, UpdateView):
    model = Post
    success_url = reverse_lazy('posts:posts_list')
    fields = ('preview_pic', 'title', 'body')
    pk_url_kwarg = 'item_pk'
    template_name_suffix = '_update_form'

