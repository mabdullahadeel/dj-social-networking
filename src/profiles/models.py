from django.db import models

from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.db.models import Q
# Create your models here.
from .utils import get_random_code


class ProfileManager(models.Manager):

    def get_all_profiles_to_invite(self, sender):
        profiles = Profile.objects.all().exclude(user=sender)
        my_profile = Profile.objects.get(user=sender)
        qs = Relationship.objects.filter(Q(sender=my_profile) | Q(receiver=my_profile))

        accepted = set([]) # 'set' takes only the unique values
        for relationship in qs:
            if relationship.status == 'accepted':
                accepted.add(relationship.receiver)
                accepted.add(relationship.sender)

        #  all the available profiles that can be added as friends
        available = [profile for profile in profiles if profile not in accepted]
        return available


    def get_all_profiles(self, me):
        profiles = Profile.objects.all().exclude(user=me)

        return profiles

# Choices --Profile
GENDER_CHOICES = (
    ('Ma', 'Male'),
    ('Fe', 'Female'),
    ('Un-Sp', 'Rather not say'), #Un-Specified
)

class Profile(models.Model):
    first_name = models.CharField(max_length=200, blank=True)
    last_name = models.CharField(max_length=200, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(default="No bio...", max_length=400)
    email = models.EmailField(max_length=200, blank=True)
    country = models.CharField(max_length=200, blank=True)

    # Install pillow
    # Create media_root
    # find avatar
    avatar = models.ImageField(default='default_avatar.png', upload_to='avatars/')
    cover_picture = models.ImageField(default='default_cover.jpg', upload_to='cover_pics/')

    friends = models.ManyToManyField(User, blank=True, related_name='friends')
    slug = models.SlugField(unique=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    # Personal Info
    gender = models.CharField(max_length=5, choices=GENDER_CHOICES, blank=True)
    # Social Info
    profession = models.CharField(max_length=15, blank=True)
    facebook_url = models.CharField(max_length=2083, blank=True)
    youtube_url = models.CharField(max_length=2083, blank=True)
    instagram_url = models.CharField(max_length=2083, blank=True)
    twitter_url = models.CharField(max_length=2083, blank=True)
    quora_url = models.CharField(max_length=2083, blank=True)

    # Extending the queryset potential
    objects = ProfileManager()

    
    def __str__(self):
        return f"{self.user.username} | {self.first_name} {self.last_name} | {self.created.strftime('%d-%m-%Y')}"

    # friends related
    def get_friends(self):  # to return the friends associated with a user
        return self.friends.all()

    def get_number_of_friends(self):   # to return the number of friends
        return self.friends.all().count()

    # post related
    def get_all_post_number(self):   #total number of post of the specific user
        return self.posts.all().count()

    def get_all_post(self):  # get all posts related to this specific profile
        return self.posts.all()

    # likes related
    def get_like_given_number(self):
        likes = self.like_set.all()
        total_likes = 0
        for like in likes:
            if like.value == 'LI':
                total_likes += 1

        return total_likes

    def get_like_received_number(self):
        all_posts = self.posts.all()
        total_likes = 0
        for item in all_posts:
            total_likes += item.number_of_likes()

        return total_likes
    

    # To prevent the overriding of existing slug on profile save
    __initial__first_name = None
    __initial__last_name = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__initial__first_name = self.first_name
        self.__initial__last_name = self.last_name

    # For two persons having same First & Last Names
    def save(self, *args, **kwargs):                                            #This method is called everytime the Profile Model saves 
        is_exist = False
        if self.first_name != self.__initial__first_name or self.last_name != self.__initial__last_name:
            if self.first_name and self.last_name:
                to_slug = slugify(str(self.first_name + " " + self.last_name))
                is_exist = Profile.objects.filter(slug=to_slug).exists()        # return true if slug already exist
                while is_exist:
                    to_slug = slugify(to_slug + " " + str(get_random_code()))   # append a random code unless the User gets unique slug
                    is_exist = Profile.objects.filter(slug=to_slug).exists()
        else:
            to_slug = str(self.user)
        
        self.slug = to_slug
        super().save(*args, **kwargs)

# Sending and Recieving Friends Requests
class RelationshipManager(models.Manager):
    def invitation_received(self, receiver):
        query_set = Relationship.objects.filter(receiver=receiver, status='send')
        return query_set


STATUS_CHOICES=(
    ('send', 'send'),
    ('accepted', 'accepted'),
)
class Relationship(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='receiver')
    status = models.CharField(max_length=8, choices=STATUS_CHOICES)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    # Exteding the query set (Manager)
    objects = RelationshipManager()

    def __str__(self):
        return f"{self.sender} - {self.receiver} | {self.status}"