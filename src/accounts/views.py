from django.shortcuts import render
from django.http import HttpResponse 
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,get_user_model
from django.utils.http import is_safe_url
from .forms import LoginForm,RegisterForm
# Create your views here.

def login_page(request):
        form=LoginForm(request.POST or None)
        context={
            "form": form
        }
        print(request.user.is_authenticated())
        if form.is_valid():
           next_=request.GET.get('next')
           next_post=request.POST.get('next')
           redirect_path=next_ or next_post or None
           username=form.cleaned_data.get("username")
           password=form.cleaned_data.get("password")
           user=authenticate(request,username=username,password=password)
           print(request.user.is_authenticated())
           if user is not None:
               print(request.user.is_authenticated())
               login(request,user)
               if is_safe_url(redirect_path,request.get_host()):
                   return redirect(redirect_path)
               else:
                   return redirect("/")
           else: 
                 print("error")
        return render(request,"accounts/login.html",context)

def register_page(request):
    form=RegisterForm(request.POST or None)
    context={
            "form": form
        }
    if form.is_valid():
           username=form.cleaned_data.get("username")
           email=form.cleaned_data.get("email")
           password=form.cleaned_data.get("password")
           new_user=user.objects.create_user(username,email,password)
        #    new_user.save() 
           print(new_user)
           print(form.cleaned_data)
           
    return render(request,"accounts/register.html",context )
