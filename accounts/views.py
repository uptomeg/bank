from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as login_user, \
                                logout as logout_user
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import FormView, UpdateView, DeleteView, CreateView
from django.views.generic.list import ListView
from .forms import LoginForm, SignupForm, EditProfileForm
from django.http import HttpResponse
from django.http import JsonResponse
from django.contrib import messages

class LoginView(FormView):
    form_class = LoginForm
    template_name = 'accounts/login.html'
    success_url = reverse_lazy('accounts:view')
    def form_valid(self, form):
        login_user(self.request, form.cleaned_data['user'])
        return super().form_valid(form) 

def logout(request):
    if request.user.is_authenticated:
        logout_user(request)
        request.session['from'] = 'logout'
    return redirect(reverse('accounts:login'))

class SignupView(CreateView):
    form_class = SignupForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('accounts:login')
    
    # note that ModelForm saves object automatically
    def form_valid(self, form):
        self.request.session['from'] = 'signup' 
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password1'])
        user.save()
        return super().form_valid(form)

def profileview(request):
    if request.user.is_authenticated:
        responseData = {
        'id': request.user.id,
        'username': request.user.username,
        'email' : request.user.email,
        'first_name' : request.user.first_name,
        'last_name' : request.user.last_name,
        }
        return JsonResponse(responseData)
    else:
        return HttpResponse('HTTP 401 UNAUTHORIZED', status=401)


""" class profileUpdate(UpdateView):
    model = User
    template_name = 'profile.html'
    fields = ['first_name', 'last_name', 'email', 'password1', 'password2']
    def get_success_url(self):
        return reverse('stores:detail', kwargs={'pk' : self.kwargs['pk']}) """


def edit_profile(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = EditProfileForm(request.POST, instance=request.user)
            if form.is_valid():
                if form.cleaned_data['password1'] != None:
                    user = form.save(commit=False)
                    user.set_password(form.cleaned_data['password1'])
                    user.save()
                else:
                    form.save()
                login_user(request, user)
                return redirect(reverse_lazy('accounts:view'))
        else:
            form = EditProfileForm(instance=request.user)
        return render(request, 'accounts/profile.html', {'form': form})
    else:
        return HttpResponse('HTTP 401 UNAUTHORIZED', status=401)