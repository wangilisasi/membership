from django.views.generic import ListView
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from membersub.models import Membership, UserMembership, Subscription
from .forms import SignUpForm
class MembershipView(ListView):
    model = Membership
    template_name = 'list.html'
    def get_user_membership(self,x):
        user_membership_qs = UserMembership.objects.filter(user=self.request.user)
        print(user_membership_qs)
        if user_membership_qs.exists():
            return user_membership_qs.first()
        return None
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        current_membership = self.get_user_membership(self.request)
        print(current_membership)
        print(current_membership.membership)
        context['current_membership'] = str(current_membership.membership)
        return context

def sign_up_user_view(request):
    context={}
    if request.POST:
        form=SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username=form.cleaned_data.get('username').lower()  #cast their email to lowercase
            raw_password=form.cleaned_data.get('password1')
            user=authenticate(username=username,password=raw_password)
            login(request,user)
            return redirect('memberships')
        else:
            context['registration_form']=form
    else:
        form = SignUpForm()
        context['registration_form']=form
    return render(request,'register.html',context)
        
def logout_view(request):
    logout(request)
    return redirect('memberships')


