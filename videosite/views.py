from django.contrib.auth import login, authenticate
from .forms import UserCreationForm, VideoUploadForm, CommentForm
from django.shortcuts import render, redirect
from .services import store_file, check_file_type, create_user, get_videos_and_categories_pair_list, store_video
from .models import Video, Category, Comment
import os


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            create_user(form, authenticate, request, login)
            return redirect('mainpage')
    else:
        form = UserCreationForm()
    return render(request, 'videosite/signup.html', {'form': form})


def mainpage(request):
    if not(request.user.is_authenticated):
        redirect('login')
    else:
        return redirect('dashboard')
    return redirect('login')


def dashboard(request):
    if not(request.user.is_authenticated):
        return redirect('login')
    else:
        return render(request, 'videosite/dashboard.html', {'videos': get_videos_and_categories_pair_list()})


def upload(request):
    if not(request.user.is_authenticated):
        redirect('login')
    else:
        if request.method == 'POST':
            form = VideoUploadForm(request.POST, request.FILES)
            if form.is_valid():
                video_store_bool = store_video(request, form)
                if(video_store_bool):
                    return render(request, 'videosite/uploadsuccess.html')
                else:
                    return render(request, 'videosite/wrongfile.html')
            return redirect('dashboard')
        else:
            form = VideoUploadForm()
        return render(request, 'videosite/upload.html', {'form': form})


def playvideo(request, video_id):
    if not(request.user.is_authenticated):
        return redirect('login')
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            Comment.objects.create(user=request.user, video=Video.objects.get(
                id=video_id), comment=form.data['comment'])
            return redirect('playvideo', video_id)
    else:
        form = CommentForm()
        video = Video.objects.prefetch_related().filter(id=video_id)
        categories = video[0].categories.all()
        uploaded_by = video[0].user.username
        comments = video[0].comments.order_by('-id')
        if(not(video)):
            return 404
        return render(request, 'videosite/videoplayer.html', {'video': video[0], 'categories': categories, 'uploaded_by': uploaded_by, 'form': form, 'comments': comments})
    return render(request, 'videosite/videoplayer.html', {'video': video[0], 'categories': categories, 'uploaded_by': uploaded_by, 'form': form, 'comments': comments})


def category(request, category):
    if not(request.user.is_authenticated):
        return redirect('login')
    category_searched = category
    categories = Category.objects.prefetch_related().filter(
        category_name__icontains=category).all()
    videos_and_categories_pair_list = []
    for category in categories:
        videos_and_categories_pair_list.append(
            (category.video, category.video.categories.all()))
    return render(request, 'videosite/search.html', {'videos': videos_and_categories_pair_list, 'category': category_searched})
