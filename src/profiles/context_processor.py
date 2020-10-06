'''
    This file contains the code for getting a particular thing fron db to be available in all the views like
    'profile picture', 'number of request' etc ---> the remaining configration is in "settings.py"
'''

from .models import Profile

def profile_pic(request):
    if request.user.is_authenticated:
        profile_obg = Profile.objects.get(user=request.user)
        profile_picture = profile_obg.avatar
        return {
            'profile_picture' : profile_picture,
        }
    return {}