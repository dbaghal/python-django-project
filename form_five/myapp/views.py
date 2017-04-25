from django.shortcuts import render
from myapp.forms import UserForm,UserProfileInfoForm


from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse,HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required



# Create your views here.


def index(request):
    return render(request,'myapp/index.html')

def register(request):
    registered = False


    if request.method=="POST":
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user

            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']
            profile.save()
            registered=True
        else:
            print(user_form.errors,profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()
    return render(request,'myapp/registration.html',{'user_form':user_form,'profile_form':profile_form,'registered':registered})


@login_required
def special(request):
    return HttpResponse('You are logged in Nice!..')


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))





def user_login(request):

    if request.method=="POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username,password=password)
        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("Account is not active")

        else:
            print("Someone try to login and failed!...")
            print("Username:{}and Password:{}".format(username,password))
            return HttpResponse("Invalid login details supplied")
    else:
        return render(request,'myapp/login.html',{})

