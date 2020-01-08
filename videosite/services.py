import magic
from .models import Video, Category


def check_file_type(f):
    magic_function = magic.Magic(mime=True, uncompress=True)
    file_head = f.read(2048)
    file_type = magic_function.from_buffer(file_head)
    if 'video' not in file_type:
        return False
    return True


def store_video(request, form):
    if(check_file_type(request.FILES['file_data'])):
        video_object = Video.objects.create(
            title=form.data['title'], user=request.user)
        store_file(
            request.FILES['file_data'], str(video_object.id))
        categories = form.data['categories'].split(',')
        category_list = []
        for category in categories:
            category_list.append(
                Category(category_name=category, video=video_object))
        Category.objects.bulk_create(category_list)
        return True
    return False


def store_file(file, file_name):
    with open('videosite/static/upload/'+file_name, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)


def create_user(form, authenticate, request, login):
    form.save()
    username = form.cleaned_data.get('username')
    raw_password = form.cleaned_data.get('password1')
    user = authenticate(username=username, password=raw_password)
    login(request, user)


def get_videos_and_categories_pair_list():
    videos = Video.objects.prefetch_related().all()
    videos_and_categories_pair_list = []
    for video in videos:
        videos_and_categories_pair_list.append(
            (video, video.categories.all()))
    return videos_and_categories_pair_list


def get_playvideo_contents(video_id):
    video = Video.objects.prefetch_related().filter(id=video_id)
    if(not(video)):
        return 0, 1, 1, 1
    categories = video[0].categories.all()
    uploaded_by = video[0].user.username
    comments = video[0].comments.order_by('-id')
    return video, categories, uploaded_by, comments


def get_videos_and_categories_pair_list_from_search(category):
    categories = Category.objects.prefetch_related().filter(
        category_name__icontains=category).all()
    videos_and_categories_pair_list = []
    for category in categories:
        videos_and_categories_pair_list.append(
            (category.video, category.video.categories.all()))
    return videos_and_categories_pair_list
