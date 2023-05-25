from django.shortcuts import render, redirect
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model, login, authenticate, logout

from account.forms import SingUpForm, LoginForm

from phone_book.models import BookOwner

User = get_user_model()

redirect_path = "/books"

def login_user(request):
    global redirect_path
    if request.user.is_authenticated:
        return redirect(redirect_path)
    form = LoginForm(request.POST or None)
    if request.POST:
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)
            # BookOwner.objects.get_or_create(
            #     user = user,
            #     status = True,
            #     is_deleted = False,
            # )
            login(request, user=user)
            return redirect(redirect_path)

    context = {
        "form": form
    }
    return render(request, "login.html", context)


def register_user(request):
    global redirect_path
    if request.user.is_authenticated:
        return redirect(redirect_path)
    form = SingUpForm(request.POST or None)
    er_message = ""
    if request.POST:
        if form.is_valid():
            username = form.cleaned_data.get("username")
            # first_name = form.cleaned_data.get("first_name")
            # last_name = form.cleaned_data.get("last_name")
            # email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            # familier = form.cleaned_data.get("familier")
            # phone = form.cleaned_data.get("phone_number")
            try:
                user = User.objects.create_user(
                    username=username, password=password
                )
                BookOwner.objects.get_or_create(
                    user = user,
                    status = True,
                    is_deleted = False,
                )
                login(request, user)
                return redirect(redirect_path)
            except:
                er_message = "مشکلی وجود دارد لطفا از راه های ارتباطی به ما اطلاع بدهید"

    context = {
        "form": form,
        "er_message": er_message
    }
    return render(request, "register.html", context)


def logout_admin(request):
    global redirect_path
    logout(request)
    return redirect(redirect_path)
