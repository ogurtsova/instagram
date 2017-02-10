from django.shortcuts import render, redirect, get_object_or_404
from app.forms import UploadFileForm, CommentForm, SignUpForm, SignInForm, SettingsForm
from app.models import Post, Comment, Profile
from .helpers import pagination, Pager
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash




def index(request):
    posts = Post.objects.all().order_by('-id')
    page = pagination(request, posts, 3)

    return render(request, 'index.html', locals())

@login_required
def upload(request):
    form = UploadFileForm()

    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            p = Post()
            p.description = request.POST['description']
            p.image = request.FILES['file']
            p.user = request.user
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
            comment.user = request.user
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
            Profile.objects.create(user=user)

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


def user_page(request, username):
    page_user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(user=page_user).order_by('-id')
    page = pagination(request, posts, 16)
    return render(request, 'user_page.html', locals())


def settings(request):
    
    initial = {
        'username': request.user.username
    }
    form = SettingsForm(initial=initial)

    if request.method == "POST":
        form = SettingsForm(request.POST, request.FILES)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            users = User.objects.filter(username=username)
            if len(users) == 0:
                request.user.username = username
            elif request.user.id != users[0].id:
                messages.add_message(request, messages.ERROR, 'Sorry, this username is taken!')
            userpic = request.FILES.get('userpic')
            if userpic is not None:
                request.user.profile.userpic = userpic
                request.user.profile.save()
            password = form.cleaned_data.get('password')
            if  password != '':
                if request.user.check_password(password):
                    new_password = form.cleaned_data.get('new_password')
                    confirm_password = form.cleaned_data.get('confirm_password')
                    if new_password != '':
                        if new_password == confirm_password:
                            request.user.set_password(new_password)
                            update_session_auth_hash(request, request.user)
                            messages.add_message(request, messages.SUCCESS, 'Password was updated')
                        else:
                            messages.add_message(request, messages.ERROR, 'Passwords do not match!')
                else:
                    messages.add_message(request, messages.ERROR, 'Wrong password!')
            request.user.save()
            return redirect(request.path)

    return render(request, 'settings.html', locals())























