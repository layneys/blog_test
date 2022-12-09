from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView
from .models import UserProfile
from .forms import UserCreateForm
from django.contrib import messages
from posts.views import UserInfoMixin
# Create your views here.


class UserCreateView(UserInfoMixin, CreateView):
    model=UserProfile
    success_url = '/'
    form_class = UserCreateForm

    def form_valid(self, form):
        c = {'form': form, }
        user = form.save(commit=False)
        first_name = form.cleaned_data['first_name']
        last_name = form.cleaned_data['last_name']
        about = form.cleaned_data['bio']
        date_birth = form.cleaned_data['date_birth']
        password1 = form.cleaned_data['password1']
        password2 = form.cleaned_data['password2']
        if password1 != password2:
            messages.error(self.request, "Passwords do not Match", extra_tags='alert alert-danger')
            return render(self.request, self.template_name, c)
        user.set_password(password1)
        user.save()

        # Create UserProfile model
        UserProfile.objects.create(user=user, first_name=first_name, last_name=last_name,
                                   bio=about, date_birth=date_birth)

        return super(UserCreateView, self).form_valid(form)


class UserProfileView(UserInfoMixin, DetailView):
    model = UserProfile
    slug_field = 'id'
    slug_url_kwarg = 'id'


class UserProfileUpdateView(UserInfoMixin, UpdateView):
    model = UserProfile
    fields = ('avatar', 'first_name', 'last_name', 'bio', 'date_birth')
    pk_url_kwarg = 'pk'
    success_url = reverse_lazy('posts:posts_list')
    template_name_suffix = '_update_form'