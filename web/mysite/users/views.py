from django.shortcuts import render
from .models import UserProfile



# Create your views here.
def user_list(request):
    users = UserProfile.objects.all()
    return render(request, 'users_list.html', {'users': users})
