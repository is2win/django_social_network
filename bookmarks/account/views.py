from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from .forms import LoginForm, UserRegistrationForm, \
    UserEditForm, ProfileEditForm
from django.contrib.auth.decorators import login_required
from .models import Profile


# def user_login(request):
#     if request.method == 'POST':
#         # создается экземпляр с данными из POST запроса
#         form = LoginForm(request.POST)
#         # Валидируем форму на наличие ошибок, ошибки добавим в шаблон
#         if form.is_valid():
#             cd = form.cleaned_data
#             # если форма валидна, происходит аутентификация пользователя в базе данных и
#             # возвращает объект User если пользователь найден или None - если нет
#             user = authenticate(request,
#                                 username=cd['username'],
#                                 password=cd['password'])
#             # пользователь найден
#             if user is not None:
#                 # Далее проверям, активен ли пользователь
#                 # is_active принадлежит объекту User модели Django
#                 if user.is_active:
#                     # вход пользователя в систему + сообщение о входе
#                     login(request, user)
#                     return HttpResponse('Authenticated successfully')
#                 # если пользователь не активен - вернуть ошибку
#                 else:
#                     return HttpResponse('Disabled account')
#             # если пользователь не был успешно аутентифицирован - возвращаем None и делаем ошибку
#             else:
#                 return HttpResponse('Invalid login')
#
#     else:
#         #  создается экземпляр формы логина
#         form = LoginForm()
#     return render(request, 'account/login.html', {'form': form})


@login_required
def dashboard(request):
    return render(request,
                  'account/dashboard.html',
                  {'section': 'dashboard'})


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # создать новый объект пользователя,
            # но пока не сохранять его
            new_user  = user_form.save(commit=False)
            # установить выбраннный пароль
            new_user.set_password(
                user_form.cleaned_data['password']
            )
            # сохранить объект User
            new_user.save()
            # создать профиль пользователя
            Profile.objects.create(user=new_user)
            return render(request,
                          'account/register_done.html',
                          {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request,
                  'account/register.html',
                  {'user_form': user_form})


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        profile_form = ProfileEditForm(
            instance=request.user.profile,
            data=request.POST,
            files=request.FILES
        )
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(
        request,
        'account/edit.html',
        {'user_form': user_form,
         'profile_form': profile_form}
    )