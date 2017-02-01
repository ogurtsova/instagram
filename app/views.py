from django.shortcuts import render, redirect, get_object_or_404
from app.forms import UploadFileForm
from app.models import Post
from .helpers import pagination, Pager

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

