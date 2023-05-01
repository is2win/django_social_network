from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from .forms import LoginForm
from django.contrib.auth.decorators import login_required


def user_login(request):
    if request.method == 'POST':
        # создается экземпляр с данными из POST запроса
        form = LoginForm(request.POST)
        # Валидируем форму на наличие ошибок, ошибки добавим в шаблон
        if form.is_valid():
            cd = form.cleaned_data
            # если форма валидна, происходит аутентификация пользователя в базе данных и
            # возвращает объект User если пользователь найден или None - если нет
            user = authenticate(request,
                                username=cd['username'],
                                password=cd['password'])
            # пользователь найден
            if user is not None:
                # Далее проверям, активен ли пользователь
                # is_active принадлежит объекту User модели Django
                if user.is_active:
                    # вход пользователя в систему + сообщение о входе
                    login(request, user)
                    return HttpResponse('Authenticated successfully')
                # если пользователь не активен - вернуть ошибку
                else:
                    return HttpResponse('Disabled account')
            # если пользователь не был успешно аутентифицирован - возвращаем None и делаем ошибку
            else:
                return HttpResponse('Invalid login')

    else:
        #  создается экземпляр формы логина
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})


@login_required
def dashboard(request):
    return render(request,
                  'account/dashboard.html',
                  {'section': 'dashboard'})