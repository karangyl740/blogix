from django.shortcuts import render, redirect
from blogs.models import Category,Blogs
from .forms import RegistrationForm
from django.contrib import auth
from django.contrib.auth.forms import AuthenticationForm
def home(request):
    categories = Category.objects.all()
    featured_post = Blogs.objects.filter(is_feacherd=True,status='published')
    posts = Blogs.objects.filter(is_feacherd=False,status='published')
    context = {
        'categories': categories,
        'featured_post':featured_post,
        'posts':posts
    }
    return render(request,"home.html",context)

def register(request):
    if request.method=="POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('register')
    else:
        form = RegistrationForm()
    context={
        'form':form
    }
    return render(request, 'register.html', context)



# login
def login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = auth.authenticate(username=username,password=password)
            if user is not None:
                auth.login(request,user)
                return redirect('dashboard')
    else:
        form = AuthenticationForm()

    context = {
        'form': form
    }
    return render(request,'login.html',context)


def logout(request):
    auth.logout(request)
    return redirect('home')

def help_center(request):
    return render(request, 'help_center.html')


from django.core.mail import send_mail
from django.conf import settings

def contact_us(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        # Example: Send email to support
        send_mail(
            subject,
            f'Message from {name} ({email}):\n\n{message}',
            email,
            [settings.DEFAULT_FROM_EMAIL],
            fail_silently=False,
        )
        return redirect('contact')  # Redirect after submission
    return render(request, 'contact_us.html')


def terms_of_service(request):
    return render(request, 'terms_of_service.html')