from django.shortcuts import render, get_object_or_404, redirect
from .forms.forms import BankForm
from .forms.branchforms import BranchForm
from .models import Bank, Branch
from django.contrib.auth.models import User
from django.views.generic import (
    ListView, DetailView, UpdateView
)
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django import forms


class AddBank(LoginRequiredMixin, FormView):
    form_class = BankForm
    template_name = 'banks/create.html'

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return HttpResponse('401 UNAUTHORIZED', status=401)
        return super().handle_no_permission()

    def form_valid(self, form):
        bank = form.save(commit=False)
        bank.owner = self.request.user
        bank.save()
        self.success_url = reverse_lazy('banks:bank_details', args=[form.instance.id])
        return super().form_valid(form)


class AddBranch(LoginRequiredMixin, FormView):
    form_class = BranchForm
    template_name = 'banks/branch.html'

    def dispatch(self, request, *args, **kwargs):
        bankd = self.kwargs.get('pk')
        if not self.request.user.is_authenticated:
            return HttpResponse('401 UNAUTHORIZED', status=401)
        try:
            bank = Bank.objects.get(id=bankd)
        except Bank.DoesNotExist:
            return HttpResponse('404 NOT FOUND', status=404)
        if not self.request.user == bank.owner:
            return HttpResponse('403 FORBIDDEN', status=403)
        return super().dispatch(request, *args, **kwargs)
        

    def form_valid(self, form):
        bank = Bank.objects.get(id=self.kwargs.get('pk'))
        branch = form.save(commit=False)
        branch.bank = bank
        branch.save()
        self.success_url = reverse_lazy('banks:branch_details', args=[form.instance.id])
        return super().form_valid(form)

    


@csrf_exempt
@require_http_methods(["GET"])
def branchdetail(request, pk):
    try:
        branch = Branch.objects.get(id=pk)
    except Branch.DoesNotExist:
        raise Http404('404 NOT FOUND')
    responseData = {
        'id': branch.id,
        'name': branch.name,
        'transit_num': branch.transit_num,
        'address': branch.address,
        'email' : branch.email,
        'capacity' : branch.capacity,
        'last_modified' : branch.last_modified.isoformat(),
    }
    return JsonResponse(responseData, safe=False)
    

@csrf_exempt
@require_http_methods(["GET"])
def allbranchdetail(request, pk):
    try:
        my_object = Bank.objects.get(id=pk)
        branches = my_object.branch_set.all()
        response = []
        for branch in branches:
            response.append({
            'id': branch.id,
            'name': branch.name,
            'transit_num': branch.transit_num,
            'address': branch.address,
            'email' : branch.email,
            'capacity' : branch.capacity,
            'last_modified' : branch.last_modified.isoformat(),
            })
        return JsonResponse(response, safe=False)
    except Bank.DoesNotExist:
        return HttpResponse('404 NOT FOUND', status=404)



class ListBank(ListView):
    queryset = Bank.objects.all()
    template_name = 'banks/list.html'


class DetailBank(DetailView):
    model = Bank
    template_name = 'banks/detail.html'

    def dispatch(self, request, *args, **kwargs):
        bankd = self.kwargs.get('pk')
        try:
            bank = Bank.objects.get(id=bankd)
        except Bank.DoesNotExist:
            return HttpResponse('404 NOT FOUND', status=404)
        return super().dispatch(request, *args, **kwargs)
        

    def get_object(self):
        bank_id = self.kwargs.get('pk')
        try:
            object = get_object_or_404(Bank, id = bank_id)
        except:
            return HttpResponse('404 NOT FOUND', status=404)
        return object


class EditBranch(LoginRequiredMixin, UpdateView):
    model = Branch
    template_name = 'banks/editbranch.html'
    fields = ['name', 'transit_num', 'address', 'email', 'capacity']
    success_url = reverse_lazy('banks:branch_details')
    error_messages = {
            'name': {'required': 'This field is required'},
            'transit_num': {'required': 'This field is required'},
            'address': {'required': 'This field is required'},
            'email': {'required': 'This field is required', 'invalid': 'Enter a valid email address'},
    } 
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['capacity'] = forms.IntegerField(required=False, min_value=0)
        return form

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponse('401 UNAUTHORIZED', status=401)
        branchid = self.kwargs.get('pk')
        try:
            branch = Branch.objects.get(id=branchid)
        except Branch.DoesNotExist:
            return HttpResponse('404 NOT FOUND', status=404)
        if not self.request.user == branch.bank.owner:
            return HttpResponse('403 FORBIDDEN', status=403)
        return super().dispatch(request, *args, **kwargs)




    """  def form_invalid(self, form):
        response = super().form_invalid(form)
        errors = form.errors
        error_dict = {}
        if form.cleaned_data.get('name') is None:
            error_dict['name'] = 'This field is required'
        if form.cleaned_data.get('transitnumber') is None:
            error_dict['transitnumber'] = 'This field is required'
        if form.cleaned_data.get('address') is None:
            error_dict['address'] = 'This field is required'
        if form.cleaned_data.get('email') is None:
            error_dict['email'] = 'This field is required'
        else:
            email = self.cleaned_data.get('email')
            try:
                validate_email(email)
            except:
                 error_dict['email'] = 'Enter a valid email address'
        response.context_data["form"].errors = error_dict
        return response """

    def get_initial(self):
        initial = super().get_initial()
        branch = self.get_object()
        initial.update({
            'name': branch.name,
            'transit_num': branch.transit_num,
            'address': branch.address,
            'email': branch.email,
            'capacity': branch.capacity
        })
        return initial
        
    def get_success_url(self):  
        return reverse('banks:branch_details', kwargs={'pk': self.object.id})
