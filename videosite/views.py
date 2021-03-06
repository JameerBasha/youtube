from django.contrib.auth import login, authenticate
from .forms import UserCreationForm, VideoUploadForm, CommentForm
from django.shortcuts import render, redirect
from .services import store_file, check_file_type, create_user, get_videos_and_categories_pair_list, store_video, get_playvideo_contents, get_videos_and_categories_pair_list_from_search
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
    return render(request, 'videosite/signup.html', {'form': form, 'title': 'SignUp'})


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
        return render(request, 'videosite/dashboard.html', {'videos': get_videos_and_categories_pair_list(), 'title': 'Youtube'})


def upload(request):
    if not(request.user.is_authenticated):
        redirect('login')
    else:
        if request.method == 'POST':
            form = VideoUploadForm(request.POST, request.FILES)
            if form.is_valid():
                video_store_bool = store_video(request, form)
                if(video_store_bool):
                    return render(request, 'videosite/uploadsuccess.html', {'title': 'Success'})
                else:
                    return render(request, 'videosite/wrongfile.html', {'title': 'Failed'})
            return redirect('dashboard')
        else:
            form = VideoUploadForm()
        return render(request, 'videosite/upload.html', {'form': form, 'title': 'Upload'})


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
        video, categories, uploaded_by, comments = get_playvideo_contents(
            video_id)
        if(not(video)):
            return render(request, 'videosite/videonotfound.html')
        return render(request, 'videosite/videoplayer.html', {'video': video[0], 'categories': categories, 'uploaded_by': uploaded_by, 'form': form, 'comments': comments, 'title': 'PlayVideo'})
    return render(request, 'videosite/videoplayer.html', {'video': video[0], 'categories': categories, 'uploaded_by': uploaded_by, 'form': form, 'comments': comments, 'title': 'PlayVideo'})


def category(request, category):
    if not(request.user.is_authenticated):
        return redirect('login')
    videos_and_categories_pair_list = get_videos_and_categories_pair_list_from_search(
        category)
    return render(request, 'videosite/search.html', {'videos': videos_and_categories_pair_list, 'category': category, 'title': 'Search'})


def error_404(request, exception):
    return render(request, 'videosite/error_404.html')


def error_500(request):
    return render(request, 'videosite/error_500.html')
