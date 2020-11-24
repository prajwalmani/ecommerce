from django.http import HttpResponse 
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,get_user_model
from .forms import ContactForm,LoginForm,RegisterForm

user=get_user_model()

def home_page(request): 
    context={
        "title":"Home Page",
        "content":"Welcome to home page",
    }
    # if request.user.is_authenticated():
        # context['premium_content':"Yaaaaaa"]
    return render(request,"home_page.html",context)

def about_page(request):
    context={
        "title":"About Page",
        "content":"Welcome to about page"

    }
    return render(request,"home_page.html",context)

def contact_page(request):
    contact_form=ContactForm(request.POST or None)
    context={
        "title":"Contact page",
        "content":"Welcome to contact page",
        "form":contact_form
    }
    if contact_form.is_valid():
        print(contact_form.cleaned_data)
    return render(request,"contact/view.html",context)    

def login_page(request):
        form=LoginForm(request.POST or None)
        context={
            "form": form
        }
        print("User logged in")
        print(request.user.is_authenticated())
        if form.is_valid():
           print(form.cleaned_data)
           username=form.cleaned_data.get("username")
           password=form.cleaned_data.get("password")
           user=authenticate(request,username=username,password=password)
           print(request.user.is_authenticated())
           if user is not None:
               print(request.user.is_authenticated())
               login(request,user)
               context['form']=LoginForm()
               return redirect("/")
           else: 
                 print("error")
        return render(request,"auth/login.html",context)

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
           
    return render(request,"auth/register.html",context )
  