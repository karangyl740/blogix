from django.shortcuts import render,redirect
from blogs.models import Blogs,Category
from django.contrib.auth.decorators import login_required
from .forms import CategoryForm,BlogPostForm
from django.shortcuts import get_object_or_404
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from .forms import AddUserForm,EditUserForm

# Create your views here.
@login_required(login_url='login')
def dashboard(request):
    category_counts=Category.objects.all().count()

    blogs_counts = Blogs.objects.all().count()

    context = {
        'category_counts':category_counts,
        'blogs_counts':blogs_counts
    }

    return render(request, 'dashboard/dashboard.html',context)

def categories(request):
    return render(request,'dashboard/categories.html')

def add_categories(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST) 
        if form.is_valid():
            form.save()
            return redirect('categories')
    form = CategoryForm()
    context = {
        'form':form
    }
    return render(request, 'dashboard/add_categories.html', context)


def edit_categories(request,pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('categories')
    form = CategoryForm(instance=category)
    context = {
        'form':form,
        'category':category
    }
    return render(request,'dashboard/edit_categories.html', context)

def delete_categories(request,pk):
    category = get_object_or_404(Category, pk=pk)
    category.delete()
    return redirect('categories')

def posts(request):
    posts = Blogs.objects.all()
    context = {
        'posts':posts
        }
    return render(request,'dashboard/posts.html', context)

def add_posts(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            title = form.cleaned_data['title']
            post.slug = slugify(title)
            post.save() 
            return redirect('posts')
        else:
            pass
    form = BlogPostForm()
    context = {
        'form':form
    }
    return render(request,'dashboard/add_posts.html',context)



def delete_posts(request,pk):
    post = get_object_or_404(Blogs,pk=pk)
    post.delete()
    return redirect('posts')

def edit_posts(request, pk):
    # Fetch the blog post by primary key (similar to edit_categories)
    post = get_object_or_404(Blogs, pk=pk)

    if request.method == 'POST':
        # Use BlogPostForm for editing (similar to CategoryForm in edit_categories)
        form = BlogPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('posts')  # Redirect to posts page after saving

    # Initialize the form with the post instance (similar to edit_categories)
    form = BlogPostForm(instance=post)
    context = {
        'form': form,
        'post': post  # Pass the post object to the template
    }
    return render(request, 'dashboard/edit_posts.html', context)



def users(request):
    users = User.objects.all()
    context = {
        'users': users
    }
    return render(request,'dashboard/users.html',context)


def add_users(request):
    if request.method=="POST":
        form = AddUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('users')
    form = AddUserForm()
    context = {
        'form':form
    }
    return render(request,'dashboard/add_users.html',context)


def edit_user(request,pk):
    user = get_object_or_404(User,pk=pk)
    if request.method == "POST":
        form = EditUserForm(request.POST,instance = user)
        if form.is_valid():
            form.save()
            return redirect('users')


    form = EditUserForm(instance = user)
    context = {
        'form':form,
        'user':user
    }
    return render(request,'dashboard/edit_user.html',context)


def delete_user(request,pk):
    user = get_object_or_404(User,pk=pk)
    user.delete()
    return redirect('users')
from blogs.models import Blogs  # Add this at the top
def posts_by_category(request, category_id):
    posts = Blogs.objects.filter(category_id=category_id)
    return render(request, 'dashboard/posts_by_category.html', {'posts': posts})
