from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.views import generic
from django.contrib.auth.models import User
from django.db.models import Q

from .models import Profile, Relationship
from .forms import ProfileModelForm


# Create your views here.

def my_profile_view(request, slug):
    profile = get_object_or_404(Profile, slug=slug)
    form = ProfileModelForm(request.POST or None, request.FILES or None, instance=profile)
    confirm = False

    is_profile_owner = False
    if request.user == profile.user:
        is_profile_owner = True


    if request.method == "POST":
        if form.is_valid():
            form.save()
            confirm = True

    context = {
        "profile" : profile,
        "form" : form,
        "confirm": confirm,
        'is_profile_owner': is_profile_owner,
    }

    return render(request, 'profiles/profile_page.html', context=context)


def invites_received_view(request):
    profile = Profile.objects.get(user=request.user)
    qs = Relationship.objects.invitation_received(receiver=profile)
    results = list(map( lambda x:x.sender, qs))
    is_empty = False

    if len(results) == 0:
        is_empty = True

    context = {
        'qs':  results,
        'is_empty': is_empty
    }

    return render(request, 'profiles/my_invitations.html', context=context)


def accept_invitation(request):
    if request.method == "POST":
        pk = request.POST.get('profile_pk')
        sender = Profile.objects.get(pk=pk)
        receiver = Profile.objects.get(user=request.user)

        relation = get_object_or_404(Relationship, sender=sender, receiver=receiver)
        if relation.status == 'send':
            relation.status = 'accepted'
            relation.save()

    return redirect('profiles:friends_request_view')

def reject_invitation(request):
    if request.method == "POST":
        pk = request.POST.get('profile_pk')
        sender = Profile.objects.get(pk=pk)
        receiver = Profile.objects.get(user=request.user)

        relation = get_object_or_404(Relationship, sender=sender, receiver=receiver)
        relation.delete()

    return redirect('profiles:friends_request_view')

# returns all the profiles available in the db except the current logged in user
def all_profiles_except_user_view(request):
    user = request.user
    qs = Profile.objects.get_all_profiles(me=user)

    context = {
        'qs':  qs
    }

    return render(request, 'profiles/profile_list.html', context=context)


# returns all the profiles available to send friends request
def profiles_available_for_friends_request(request):
    user = request.user
    qs = Profile.objects.get_all_profiles_to_invite(sender=user)

    context = {
        'qs':  qs
    }

    return render(request, 'profiles/to_invite_list.html', context=context)


class ProfileListView(generic.ListView):
    model = Profile
    template_name = 'profiles/profile_list.html'
    context_object_name = 'qs'

    def get_queryset(self):
        qs = Profile.objects.get_all_profiles(me=self.request.user)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(username__iexact=self.request.user)
        profile = Profile.objects.get(user=user)

        relationship_receiver = Relationship.objects.filter(sender=profile)
        relationship_sender = Relationship.objects.filter(receiver=profile)

        rel_receiver = []
        rel_sender = []

        for item in relationship_receiver:
            rel_receiver.append(item.receiver.user)
        
        for item in relationship_sender:
            rel_sender.append(item.sender.user)

        context['rel_receiver'] = rel_receiver
        context['rel_sender'] = rel_sender
        
        context['is_empty'] = False
        if len(self.get_queryset()) == 0:
            context['is_empty'] = True

        return context


def send_friend_request(request):
    if request.method == 'POST':
        pk = request.POST.get('profile_pk')
        user = request.user
        sender = Profile.objects.get(user=user)
        receiver = Profile.objects.get(pk=pk)

        relation = Relationship.objects.create(sender=sender, receiver=receiver, status='send')

        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('posts:home_post_view')

def unfriend(request):
    if request.method == 'POST':
        pk = request.POST.get('profile_pk')
        user = request.user
        sender = Profile.objects.get(user=user)
        receiver = Profile.objects.get(pk=pk)

        relation = Relationship.objects.filter(
            (Q(sender=sender) & Q(receiver=receiver)) | #we invited someone --send friend request and it get accepted
            (Q(sender=receiver) & Q(receiver=sender))  # other person sent request and we accept
        )
        relation.delete() # we also need signals to remove the persons from eachotehr's friends list
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('posts:home_post_view')
