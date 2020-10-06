from . import views
from django.urls import path

app_name='profiles'
urlpatterns= [
    path('<str:slug>/', views.my_profile_view, name='profile'),
    path('profiles/friend-requests/', views.invites_received_view, name='friends_request_view'),
    path('profiles/all-profiles', views.all_profiles_except_user_view, name='all_profiles'),
    path('profiles/to-invite', views.ProfileListView.as_view(), name='all_available_profiles'),
    path('profiles/send-invite', views.send_friend_request, name='send_friend_request'),
    path('profiles/unfriend', views.unfriend, name='unfriend'),

    # Accept and Reject Friend Request
    path('requests/accept/', views.accept_invitation, name='accept_request'),
    path('requests/reject/', views.reject_invitation, name='reject_request'),
]