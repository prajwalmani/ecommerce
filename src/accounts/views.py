from django.shortcuts import render
from django.http import HttpResponse 
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,get_user_model
from django.utils.http import is_safe_url
from .forms import LoginForm,RegisterForm,GuestForm 
from .models import GuestEmail
# Create your views here.

def guest_register_view(request):
        form=GuestFrom(request.POST or None)
        context={
            "form": form
        }
        print(request.user.is_authenticated())
        next_=request.GET.get('next')
        next_post=request.POST.get('next')
        redirect_path=next_ or next_post or None
        if form.is_valid():
           email=form.cleaned_data.get("email")
           new_guest_email=GuestEmail.objects.create(email=email)
           request.session['guest_email_id']=new_guest_email.guest_email_id
           if is_safe_url(redirect_path,request.get_host()):
               return redirect(redirect_path)
           else:
               return redirect("/register/")         
        return redirect("/register/")
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
               try:
                   del request.session['guest_email_id']
               except:
                    pass
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
