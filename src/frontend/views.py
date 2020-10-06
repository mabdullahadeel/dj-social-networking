from django.shortcuts import render

from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.
def home_view(request):
    user = request.user
    context = {
        "user" : user,
        "message": f"Hello From {user}",
    }
    return render(request, 'frontend/home.html', context=context)