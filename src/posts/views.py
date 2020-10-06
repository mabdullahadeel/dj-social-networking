from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


from .models import Post, Like
from profiles.models import Profile
from .forms import PostModelForm, CommentModelForm

# Class Based Views
from django.views import generic
from django.contrib import messages

@login_required
def post_comment_create_list_view(request):
    post_data = Post.objects.all()
    profile = Profile.objects.get(user= request.user)

    # post Form, Comment form
    post_form = PostModelForm()
    comment_form = CommentModelForm()
    post_added = False

    user = Profile.objects.get(user=request.user)
    
    if 'submit_post_form' in request.POST:
        post_form = PostModelForm(request.POST, request.FILES)
        if post_form.is_valid():
            instance = post_form.save(commit=False)
            instance.author = user
            instance.save()
            post_form = PostModelForm()
            post_added= True

    if 'submit_comment_form' in request.POST:
        comment_form = CommentModelForm(request.POST)
        if comment_form.is_valid():
            instance = comment_form.save(commit=False)
            instance.user = user
            instance.post = Post.objects.get(id=request.POST['post_id'])
            instance.save()
            comment_form = CommentModelForm()
            return redirect('posts:home_post_view')

    context = {
        "post_data" : post_data,
        "profile" : profile,
        "post_create_form": post_form,
        "comment_form": comment_form,
        "post_added": post_added
    }

    return render(request, 'posts/main.html', context=context)

@login_required
def like_unlike_view(request):
    user = request.user
    if request.method == "POST":
        post_id = request.POST.get('post_id')
        post_obj = Post.objects.get(id=post_id)
        profile = Profile.objects.get(user=user)

        if profile in post_obj.liked.all():
            post_obj.liked.remove(profile)
        else:
            post_obj.liked.add(profile)
        
        like, created = Like.objects.get_or_create(user=profile, post_id=post_id)

    if not created:
        if like.value == 'LI':
            like.value == 'UN-L'
        else:
            like.value='LI'
    else:
        like.value='LI'
        post_obj.save()
        like.save()

    data = {
        "value" : like.value,
        "likes" : post_obj.liked.all().count()
    }

    return JsonResponse(data, safe=False)


    return redirect('posts:home_post_view')

class PostDeleteView(LoginRequiredMixin ,generic.DeleteView):
    model = Post
    template_name = 'posts/confirm_delete.html'
    success_url = reverse_lazy('posts:home_post_view')

    def get_object(self, *args, **kwargs):
        pk = self.kwargs.get('pk')      # Getting the key from the url
        obj = Post.objects.get(pk=pk)

        if not obj.author.user == self.request.user:
            messages.warning(self.request, 'You need to be the owner of this post to Delete it')
        return obj

class PostUpdateView(LoginRequiredMixin ,generic.UpdateView):
    model = Post
    form_class = PostModelForm
    template_name = 'posts/update.html'
    success_url = reverse_lazy('posts:home_post_view')

    def form_valid(self, form):
        profile = Profile.objects.get(user=self.request.user)

        if form.instance.author == profile:
            return super().form_valid(form)
        else:
            form.add_error(None, 'You need to be the owner of this post to Update it')
            return super().form_invalid(form)

