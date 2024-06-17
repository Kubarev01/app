
from django.contrib.auth.decorators import login_required

from django.contrib import auth, messages
from django.forms import CharField
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import  reverse


from users.forms import UserLoginForm, UserProfileForm, UserRegistrationForm

# Create your views here.

def login(request):
    if request.method=='POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user= auth.authenticate(username=username,password=password)
            if user:
                auth.login(request, user)
                messages.success(request,f"{user.username}, вы успешно авторизовались!")
                
                if request.POST.get('next',None):
                    return HttpResponseRedirect(request.POST.get('next'))
                
                return HttpResponseRedirect(reverse('main:index'))

    else:
        form = UserLoginForm()
    context={
        'title':'Home - Авторизация',
        'form':form
    }
    return render(request,'users/login.html',context)

def registration(request):
     
    if request.method=='POST':
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
                form.save()
                user= form.instance
                auth.login(request,user)
                messages.success(request,f"{user.username}, вы авторизовались!")
                return HttpResponseRedirect(reverse('main:index'))

    else:
        form = UserRegistrationForm()

    context = {
        'title':'Home - Регистрация',
        'form':form
    }
    return render(request,'users/registration.html',context)


@login_required()
def profile(request):
    if request.method=='POST':
        form = UserProfileForm(data=request.POST,instance=request.user,files=request.FILES )
        if form.is_valid():
                messages.success(request,f"Данные обновлены")
                form.save()
                return HttpResponseRedirect(reverse('user:profile'))

    else:
        form = UserProfileForm(instance=request.user)

    context = {
        'title':'Home - Профиль',
        'form':form
    }
    return render(request,'users/profile.html',context)

def user_cart(request):
    return render(request,'users/user_cart.html')


@login_required()
def logout(request): 
   messages.success(request,f"{request.user.username}, вы вышли из аккаунта!")
   
   auth.logout(request)
   return redirect('main:index')

