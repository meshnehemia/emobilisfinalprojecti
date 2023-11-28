import requests
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from googleapiclient.discovery import build

from entertainment.forms import VideoForm
from entertainment.models import MyVideos, Views, VideoSale
from library.credentials import MpesaAccessToken, LipanaMpesaPpassword

# Create your views here.
# API_KEY = 'AIzaSyCYi5viDwayCM4yCMuGSBQI2_W0HQlcU0U'
API_KEY = 'AIzaSyCxYuPnvD8a7NqQdFYRmxGmJRH-uDqFav8'
youtube = build('youtube', 'v3', developerKey=API_KEY)


@login_required(login_url='login')
def home(request):
    priority = []
    videoss = arrange_youtube_data("mission impossible")
    videos = MyVideos.objects.all().order_by('-updated')
    if len(videos) > 0:
        for video in videos[:4]:
            priority.append({
                "url": '/entertainment/video/' + str(video.id)+'/',
                "title": video.video_title,
                "channel": str(video.video_owner),
                "thumbnail": video.video_image.url,
                "description": video.video_description,
                "published_at": video.created
            })

    if len(priority) < 3:
        for video in videoss[:4]:
            priority.append(video)

    context = {'videos': videos, 'response': videoss, 'priority': priority}
    return render(request, 'entertainment/index.html', context)


def data(query):
    request = youtube.search().list(
        part='snippet',
        q=query,
        type='video',
        maxResults=20
    )

    return request.execute()


def arrange_youtube_data(query):
    response = data(query)
    video = []
    for item in response['items']:
        video.append({
            "url": f"https://www.youtube.com/embed/{item['id']['videoId']}",
            "title": item['snippet']['title'],
            "channel": item['snippet']['channelTitle'],
            "thumbnail": item['snippet']['thumbnails']['medium']['url'],
            "description": item['snippet']['description'],
            "published_at": item['snippet']['publishedAt']
        })
    return video


@login_required(login_url='login')
def searchdata(request):
    priority = []
    query = request.GET['query']
    videos = MyVideos.objects.filter(
        Q(type__icontains=query) |
        Q(video_title__icontains=query) |
        Q(video_owner__username__icontains=query) |
        Q(video_description__icontains=query)
    )
    if len(videos) > 0:
        for video in videos[:4]:
            priority.append({
                "url": '/entertainment/video/' + str(video.id),
                "title": video.video_title,
                "channel": str(video.video_owner),
                "thumbnail": video.video_image.url,
                "description": video.video_description,
                "published_at": video.created
            })
    videoss = arrange_youtube_data(query)
    if len(priority) < 3:
        for video in videoss[:4]:
            priority.append(video)

    context = {'videos': videos, 'response': videoss, 'priority': priority}
    return render(request, 'entertainment/index.html', context)


# @csrf_exempt
# @login_required(login_url='login')
# def upload_video(request):
#     if request.method == 'POST':
#         form = VideoForm(request.POST, request.FILES)
#         if form.is_valid():
#             video_instance = form.save(commit=False)
#             allowed_video_types = ['video/mp4', 'video/webm', 'video/ogg']
#             if video_instance.video.file.content_type not in allowed_video_types:
#                 return HttpResponseBadRequest(
#                     'Invalid video file type. Please upload a video in MP4, WebM, or Ogg format.')
#             allowed_image_types = ['image/jpeg', 'image/png', 'image/gif']
#             if video_instance.video_image and video_instance.video_image.file.content_type not in allowed_image_types:
#                 return HttpResponseBadRequest(
#                     'Invalid image file type. Please upload an image in JPEG, PNG, or GIF format for the video cover.')
#             existing_video = MyVideos.objects.filter(video_owner=request.user,
#                                                      video_title=form.cleaned_data['video_title'])
#             if existing_video.exists():
#                 return HttpResponseBadRequest('You have already uploaded this video.')
#
#             video_instance.video_owner = request.user
#             video_instance.save()
#             return JsonResponse({'success': 'success'})
#         else:
#             return form.errors
#     else:
#         form = VideoForm()
#
#     return render(request, 'entertainment/videoUpload.html', {'form': form})


@csrf_exempt
@login_required(login_url='login')
def upload_video(request):
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            video_instance = form.save(commit=False)
            allowed_video_types = ['video/mp4', 'video/webm', 'video/ogg']
            if video_instance.video.file.content_type not in allowed_video_types:
                return JsonResponse({'error': 'Invalid video file type. Please upload a video in MP4, WebM, or Ogg '
                                              'format.'})
            allowed_image_types = ['image/jpeg', 'image/png', 'image/gif']
            if video_instance.video_image and video_instance.video_image.file.content_type not in allowed_image_types:
                return JsonResponse({'error': 'Invalid image file type. Please upload an image in JPEG, PNG, or GIF '
                                              'format for the video cover.'})
            existing_video = MyVideos.objects.filter(video_owner=request.user,
                                                     video_title=form.cleaned_data['video_title'])
            if existing_video.exists():
                return JsonResponse({'error': 'You have already uploaded this video.'})

            video_instance.video_owner = request.user
            video_instance.save()

            return JsonResponse({'success': 'Video uploaded successfully'})
        else:
            return JsonResponse({'error': form.errors}, status=400)
    else:
        form = VideoForm()

    return render(request, 'entertainment/videoUpload.html', {'form': form})


@csrf_exempt
def update_video(request, video_id):
    video_instance = get_object_or_404(MyVideos, id=video_id, video_owner=request.user)

    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES, instance=video_instance)

        if form.is_valid():
            updated_video = form.save(commit=False)

            # allowed_video_types = ['video/mp4', 'video/webm', 'video/ogg']
            # if video_instance.video.file.content_type not in allowed_video_types:
            #     return JsonResponse({'error': 'Invalid video file type. Please upload a video in MP4, WebM, or Ogg '
            #                                   'format.'})

            # allowed_image_types = ['image/jpeg', 'image/png', 'image/gif']
            # if updated_video.video_image and updated_video.video_image.file.content_type not in allowed_image_types:
            #     return JsonResponse({'error': 'Invalid image file type. Please upload an image in JPEG, PNG, or GIF '
            #                                   'format for the video cover.'})

            updated_video.save()
            videos = MyVideos.objects.filter(video_owner=request.user)
            context = {'videos': videos}
            return render(request, 'entertainment/myprofile.html', context)
    else:
        form = VideoForm(instance=video_instance)

    return render(request, 'entertainment/updateVideo.html', {'form': form, 'video_instance': video_instance})


def profile(request):
    videos = MyVideos.objects.filter(video_owner=request.user)
    context = {'videos': videos}
    return render(request, 'entertainment/myprofile.html', context)


def videouserprofile(request, pk):
    videos = MyVideos.objects.filter(video_owner_id=pk)
    context = {'videos': videos}
    return render(request, 'entertainment/myprofile.html', context)


def videodetails(request, pk):
    video = get_object_or_404(MyVideos, id=pk)
    try:
        bought = VideoSale.objects.get(video=video, buyer=request.user)
    except VideoSale.DoesNotExist:
        bought = ''
    views_count = Views.objects.filter(video=video).count()
    context = {'video': video, 'views_count': views_count, 'bought': bought}
    return render(request, 'entertainment/videodetails.html', context)


def videowatch(request, pk):
    video = get_object_or_404(MyVideos, id=pk)
    Views.objects.get_or_create(video=video, user=request.user)
    return render(request, 'entertainment/watchvideo.html', {"video": video})


@csrf_exempt
def deletevideo(request, pk):
    video = get_object_or_404(MyVideos, id=pk)
    if request.method == 'POST':
        video.delete()
        return profile(request)
    context = {"obj": video.video_title}
    return render(request, 'entertainment/deletevideo.html', context)


def sales(request, pk):
    sales = VideoSale.objects.filter(video_id=pk)
    return render(request, 'entertainment/salestable.html', {'sales': sales})


@csrf_exempt
def buyvideo(request, pk):
    video = get_object_or_404(MyVideos, pk=pk)
    try:
        bought = VideoSale.objects.get(video=video, buyer=request.user)
    except VideoSale.DoesNotExist:
        bought = ''
    views_count = Views.objects.filter(video=video).count()

    context = {"video": video, "views_count": views_count, 'bought': bought}
    if request.method == 'POST':
        phone = request.POST['phone']
        amount = int(video.cost)
        access_token = MpesaAccessToken.validated_mpesa_access_token
        api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
        headers = {"Authorization": "Bearer %s" % access_token}
        mpesa_request = {
            "BusinessShortCode": LipanaMpesaPpassword.Business_short_code,
            "Password": LipanaMpesaPpassword.decode_password,
            "Timestamp": LipanaMpesaPpassword.lipa_time,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,
            "PartyA": 254757316903,
            "PartyB": LipanaMpesaPpassword.Business_short_code,
            "PhoneNumber": phone,
            "CallBackURL": "https://a8f3-102-215-13-135.ngrok-free.app/mpesa-callback/",
            "AccountReference": f"mesh Entertinment: username: {request.user.username}: title {video.video_title}",
            "TransactionDesc": "Web Development Charges"
        }
        requests.post(api_url, json=mpesa_request, headers=headers)
        VideoSale.objects.get_or_create(
            buyer=request.user,
            seller=video.video_owner,
            video=video,
            cost=amount
        )
        return render(request, 'entertainment/videodetails.html', context)

    return render(request, 'entertainment/buyvideo.html', context)
