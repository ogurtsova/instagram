from django.shortcuts import render, redirect, get_object_or_404
from app.forms import UploadFileForm, CommentForm, SignUpForm, SignInForm
from app.models import Post, Comment
from .helpers import pagination, Pager
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout




def index(request):
    posts = Post.objects.all().order_by('-id')
    page = pagination(request, posts, 3)

    return render(request, 'index.html', locals())


def upload(request):
    form = UploadFileForm()

    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            p = Post()
            p.description = request.POST['description']
            p.image = request.FILES['file']
            p.save()
            return redirect('/')

    return render(request, 'upload.html', {'form':form})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = Comment.objects.filter(post=post).order_by('-created_date')
    comment_form = CommentForm()
    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect(request.path)
    page = pagination(request, comments, 5)

    return render(request, 'post_detail.html', {'post': post, 'comment_form': comment_form, 'page':page})


def sign_up(request):
    form = SignUpForm()

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = User()
            user.username = form.cleaned_data.get("username")
            user.email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user.set_password(password)
            user.save()

            return redirect('/')

    return render(request, 'sign_up.html', locals())



def sign_in(request):
    form = SignInForm()

    if request.method == "POST":
        form = SignInForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/")

    return render(request, 'sign_in.html', locals())

def sign_out(request):
    logout(request)
    return redirect("/")
