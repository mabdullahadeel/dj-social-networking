from django.contrib import admin

# Register your models here.
from .models import Profile , Relationship

from django.forms import TextInput, Textarea
from django.db import models

class ProfileModelAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'100'})},
        models.TextField: {'widget': Textarea(attrs={'rows':25, 'cols':100})},
    }

admin.site.register(Profile, ProfileModelAdmin)
admin.site.register(Relationship)