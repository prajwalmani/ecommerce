from django.http import HttpResponse 
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,get_user_model
from .forms import ContactForm

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


  