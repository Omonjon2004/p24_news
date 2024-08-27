from threading import activeCount

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.cache import cache
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View

from apps.account.forms import SubscribeForm, FeedForm, LoginForm
from apps.account.models import Account
from apps.article.models import Article


class SubscribeView(View):
    def get(self, request):
        form = SubscribeForm()
        context = {
            "form": form
        }
        return render(request, "account/subscribe.html", context)

    def post(self, request):
        form = SubscribeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("article:home")
        else:
            context = {
                "form": form
            }
            return render(request, "account/subscribe.html", context)

class FeedView(LoginRequiredMixin, View):
    def get(self, request):
        form = FeedForm()
        return render(request, "account/contact.html", {"form": form})

    def post(self, request):
        form = FeedForm(data=request.POST)
        if form.is_valid():
            form.save(user=request.user)
            messages.info(request, "You feed successfully created ")
        else:
            return render(request, "account/contact.html", {"form": form})

class LoginView(View):
    def get(self, request):
        form = LoginForm()
        context = {
            "form": form
        }
        return render(request, "account/login.html", context=context)

    def post(self, request):
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data["username"], password=form.cleaned_data["password"])

            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {user.username}.")
                return redirect("article:home")
            else:
                messages.warning(request, "With given data user not found")
                return redirect("article:home")

class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        return redirect("article:home")

# class ActivateView(View):
#     def get(self, request, *args, **kwargs):
#         token = kwargs.get('token')
#         account = get_object_or_404(Account, activation_token=token)
#         account.is_active = True
#         account.save()
#         messages.success(request, f"Your account has been successfully activated, {account.username}")
#         return redirect("article:home")

class VerifyView(View):
    def get(self, request):
        return render(request, 'account/verify.html')

    def post(self, request):
        email = request.POST.get('email')
        entered_code = request.POST.get('code')


        cached_code = cache.get(f'verification_code_{email}')

        print(f'Email: {email}, Code: {entered_code}')
        print(cached_code)

        if  cached_code and cached_code == entered_code:
            user = Account.objects.get(email=email)
            user.is_active = True
            user.save()
            messages.success(request, "Your account has been activated successfully!")
            return redirect('article:home')
        else:
            messages.error(request, "Invalid code")
            return render(request, 'account/verify.html')


