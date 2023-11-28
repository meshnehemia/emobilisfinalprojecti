from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.http import JsonResponse
import random
import time
from agora_token_builder import RtcTokenBuilder
from .models import RoomMember
import json
from django.views.decorators.csrf import csrf_exempt
from socialmedia import views


# Create your views here.
@login_required(login_url='login')
def lobby(request):

    return render(request, 'videocall/lobby.html')

@login_required(login_url='login')
def room(request):
    return render(request, 'videocall/room.html')

@login_required(login_url='login')
def getToken(request):
    appId = "d308560eaf464fcb9eeb94338a07dce3"
    appCertificate = "7bbfeb219c944c798d1bcfd8a8347225"
    channelName = request.GET.get('channel')
    uid = random.randint(1, 230)
    expirationTimeInSeconds = 3600
    currentTimeStamp = int(time.time())
    privilegeExpiredTs = currentTimeStamp + expirationTimeInSeconds
    role = 1

    token = RtcTokenBuilder.buildTokenWithUid(appId, appCertificate, channelName, uid, role, privilegeExpiredTs)

    return JsonResponse({'token': token, 'uid': uid}, safe=False)


from django.http import JsonResponse
@login_required(login_url='login')
@csrf_exempt
def createMember(request):
    try:
        data = json.loads(request.body)
        name = data.get('name')
        uid = data.get('UID')
        room_name = data.get('room_name')

        if name and uid and room_name:
            member, created = RoomMember.objects.get_or_create(
                name=name,
                uid=uid,
                room_name=room_name
            )
            return JsonResponse({'name': name}, safe=False)
        else:
            return JsonResponse({'error': 'Missing data fields'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
@login_required(login_url='login')
def getMember(request):
    uid = request.GET.get('UID')
    room_name = request.GET.get('room_name')

    try:
        member = RoomMember.objects.get(uid=uid, room_name=room_name)
        return JsonResponse({'name': member.name}, safe=False)
    except ObjectDoesNotExist:
        return JsonResponse({'error': 'Member not found'}, status=404)  # Return a 404 Not Found status if the member doesn't exist
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)  # Handle other exceptions with a 500 Internal Server Error
@login_required(login_url='login')
@csrf_exempt
def deleteMember(request):
    data = json.loads(request.body)
    member = RoomMember.objects.get(
        name=data['name'],
        uid=data['UID'],
        room_name=data['room_name']
    )
    member.delete()
    return JsonResponse('Member deleted', safe=False)
