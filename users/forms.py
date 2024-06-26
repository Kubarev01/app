from django import forms
from django.contrib.auth.forms import AuthenticationForm

from users.models import User

#Перенимаются ограничения(валидаторы из модели User) для формы
class UserLoginForm(AuthenticationForm):

    class Meta:
        model = User
        fields=['username', 'password']

    username = forms.CharField()
    password = forms.CharField()
    

    # username = forms.CharField(
    #     label='Имя пользователя',
    #     widget=forms.TextInput(attrs={"autofocus": True,
    #                                                          "class":"form-control",
    #                                                          "placeholder":"Введите ваш логин"
                                                             
    #                                                          }))
    # password = forms.CharField(
    #     label='Пароль',
    #     widget=forms.PasswordInput(attrs={"autocomplete": "current-password",
    #                                       "class":"form-control",
    #                                       "placeholder":"Введите пароль"}),
    # )

 