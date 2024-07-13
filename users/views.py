
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView 
from django.contrib import auth, messages
from django.db.models import Prefetch
from django.forms import CharField
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import  reverse, reverse_lazy


from carts.models import Cart
from orders.models import Order, OrderItem
from users.forms import UserLoginForm, UserProfileForm, UserRegistrationForm

# Create your views here.

class UserLoginView(LoginView):
     template_name='users/login.html'
     #вместо модели привязка к форме
     form_class=UserLoginForm
     #куда перекидывать в случае успеха
     #success_url= reverse_lazy('main:index')

     def get_success_url(self) -> str:
          redirect_page=self.request.POST.get('next',None)
          if redirect_page and redirect_page!=reverse_lazy('user:logout'):
               return redirect_page
          
          return reverse_lazy('main:index')

     def get_context_data(self, **kwargs: reverse_lazy):
        context=super().get_context_data(**kwargs)
        context['title']='HOME - Авторизация'
        return context

# def login(request):
#     if request.method=='POST':
#         form = UserLoginForm(data=request.POST)
#         if form.is_valid():
#             username = request.POST['username']
#             password = request.POST['password']
#             user= auth.authenticate(username=username,password=password)

#             session_key=request.session.session_key

#             if user:
#                 auth.login(request, user)
#                 messages.success(request,f"{user.username}, вы успешно авторизовались!")
                
#                 if session_key:
#                     Cart.objects.filter(session_key=session_key).update(user=user)

#                 if request.POST.get('next',None) and request.POST.get('next',None)!=reverse("user:logout"):
#                     return HttpResponseRedirect(request.POST.get('next'))
                
#                 return HttpResponseRedirect(reverse('main:index'))

#     else:
#         form = UserLoginForm()
#     context={
#         'title':'Home - Авторизация',
#         'form':form
#     }
#     return render(request,'users/login.html',context)

def registration(request):
     
    if request.method=='POST':
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
                form.save()

                session_key=request.session.session_key

                user= form.instance
                auth.login(request,user)

                if session_key:
                    Cart.objects.filter(session_key=session_key).update(user=user)


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

    orders = Order.objects.filter(user=request.user).prefetch_related(
                Prefetch(
                    "orderitem_set",
                    queryset=OrderItem.objects.select_related("product"),
                )
            ).order_by("-id")


    context = {
        'title':'Home - Профиль',
        'form':form,
        'orders': orders,
    }
    return render(request,'users/profile.html',context)

def user_cart(request):
    return render(request,'users/user_cart.html')


@login_required()
def logout(request): 
   messages.success(request,f"{request.user.username}, вы вышли из аккаунта!")
   
   auth.logout(request)
   return redirect('main:index')

