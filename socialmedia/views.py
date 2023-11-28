from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.db.models import Q
from django.utils.timesince import timesince
from django.views.decorators.csrf import csrf_exempt
# from django.views.static import serve

# from finalemobilisprojrct import settings
from .models import Room, Topic, Message, User, PersonalChat, GroupMembers, GroupMessages, Groups
from django.http import HttpResponse, JsonResponse, Http404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .forms import RoomForm, userForm, MyUserCreationForm, CreateGroup


# Create your views here.

# rooms =[
#     {'id':1,'name':'lets learn python'},
#     {'id':2,'name':'design with me'},
#     {'id':3,'name':'fronted developer'},
# ]
@csrf_exempt
def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')
        try:
            user = User.objects.get(email=email)
        except:
            return render(request, 'socialmedia/login_error.html', {"message": 'user does not exist'})
            # messages.error(request, 'user does not exist')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'socialmedia/login_error.html', {"message": 'username and password does not match'})
            # messages.error(request, 'username and password does not match')
    context = {'page': page}
    return render(request, 'socialmedia/login_register.html', context)


@csrf_exempt
def logoutUser(request):
    logout(request)
    return redirect('home')


@csrf_exempt
def registerPage(request):
    form = MyUserCreationForm()
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.email = user.email.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'socialmedia/login_error.html', {"message": form.errors})

            # messages.error(request, form.errors)

    return render(request, 'socialmedia/login_register.html', {'form': form})


@csrf_exempt
def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )
    topics = Topic.objects.all()[0:5]
    room_count = rooms.count()
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))
    context = {'rooms': rooms, 'topics': topics, 'room_count': room_count, "room_messages": room_messages}
    return render(request, 'socialmedia/home.html', context)


@login_required(login_url='login')
@csrf_exempt
def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all().order_by('-created')
    participants = room.participants.all()
    if request.method == 'POST':
        body = request.POST.get('body')
        if body:
            # return render(request,'socialmedia/login_error.html', {"message":"arrived"})
            message = Message.objects.create(
                user=request.user,
                room=room,
                body=request.POST.get('body')

            )
            room.participants.add(request.user)
        return redirect('room', pk=room.id)

    context = {'rooms': room, 'room_messages': room_messages, 'participants': participants}
    return render(request, 'socialmedia/room.html', context)


@login_required(login_url='login')
@csrf_exempt
def userProfile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {'user': user, 'rooms': rooms, 'room_messages': room_messages, 'topics': topics}
    return render(request, 'socialmedia/profile.html', context)


@csrf_exempt
@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description'),
        )
        return redirect('home')
    context = {'form': form, 'topics': topics}
    return render(request, 'socialmedia/room_form.html', context)


@csrf_exempt
@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()
    if request.user != room.host:
        return HttpResponse("you are not allowed to use this site")

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.topic = topic
        room.name = request.POST.get('name')
        room.description = request.POST.get('description')
        room.save()

        # form =RoomForm(request.POST,instance= room)
        return redirect('home')

    context = {'form': form, "topics": topics, "room": room}
    return render(request, 'socialmedia/room_form.html', context)


@login_required(login_url='login')
@csrf_exempt
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'socialmedia/delete.html', {'obj': room})


def navbar(request):
    return render(request, 'navbar.html')


@login_required(login_url='login')
@csrf_exempt
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)
    if request.method == 'POST':
        message.delete()
        return redirect('home')
    return render(request, 'socialmedia/delete.html', {'obj': message})


@csrf_exempt
@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = userForm(instance=user)
    context = {'form': form}
    if request.method == 'POST':
        form = userForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)
    return render(request, 'socialmedia/update-user.html', context)


@csrf_exempt
def topicsPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(name__icontains=q)
    context = {'topics': topics}
    return render(request, 'socialmedia/topics.html', context)


@csrf_exempt
def activityPage(request):
    room_messages = Message.objects.all()[0:4]
    context = {'room_messages': room_messages}
    return render(request, 'socialmedia/activity.html', context)


# def authenticated_user(request):
#     if request.user.is_authenticated:
#         return request.user
#     return render(request, 'socialmedia/login_register.html', context)


from django.http import JsonResponse


@login_required(login_url='login')
@csrf_exempt
def chatting(request, pk):
    room_messages = Message.objects.filter(room_id=pk)

    # Serialize messages to JSON
    messages_data = [
        {
            'img': message.user.avator.url,
            'userid': message.user.id,
            'username': message.user.username,
            'body': message.body,
            'created': timesince(message.created),
            'messageid': message.id,
            'messagebody': message.body,
            "user": request.user.username,
            "myroom": message.room.id
        } for message in room_messages
    ]

    return JsonResponse({'messages': messages_data})

    # 'userid': message.user.id,
    # 'img': message.user.avator.url,
    # 'username': message.user.username,
    # 'body': message.body,
    # 'created': message.created,
    # 'messageid': message.id,
    # 'messagebody': message.body,

    # return JsonResponse({'messages': messages_data})


# def custom_media_serve(request, path):
#     try:
#         return serve(request, path, document_root=settings.MEDIA_ROOT)
#     except Http404:
#         # Handle the 404 response for media files here
#         return render(request, '404_media.html', status=404)


@login_required(login_url='login')
@csrf_exempt
def Mychats(request, type):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )
    topics = Topic.objects.all()[0:5]
    room_count = rooms.count()
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))
    if type == 'individual':
        mychats = PersonalChat.objects.filter(Q(sender=request.user) | Q(receiver=request.user)).distinct().order_by(
            '-time')

        mychat = [
            {
                'sendername': i.sender.username,
                'senderid': i.sender.id,
                'receiver': i.receiver.username,
                'receiverid': i.receiver.id,
                'sendericon': i.sender.avator.url,
                'message': i.message,
                'receivericon': i.sender.avator.url,
                'time': timesince(i.time)
            } for i in mychats
        ]

    else:
        mychats = GroupMembers.objects.filter(member=request.user).order_by('-id')

        mychat = [
            {
                'groupname': i.group.name,
                'icon': i.group.icon.url,
                'time': timesince(i.group.created),
                'members': GroupMembers.objects.filter(group=i.group).count(),
                'groupid': i.group.id,
                'code': i.group.groupcode
            } for i in mychats
        ]
    if request.method == 'POST':
        username = request.POST.get('search')
        username = username.lower()
        try:
            if username:
                person = User.objects.get(username=username)
                pk = person.id
                if person:
                    return redirect('/chatscreem/' + str(pk) + '/')
                else:
                    redirect('/groupchatscrean/' + str(pk) + '/')
        except ObjectDoesNotExist:
            pk = username
            return redirect('/groupchatscrean/' + str(pk) + '/')

    context = {'rooms': rooms, 'mychats': mychat, 'topics': topics, 'group_participants': room_count,
               "room_messages": room_messages, 'type': type}
    return render(request, 'socialmedia/mychats.html', context)


@login_required(login_url='login')
@csrf_exempt
def chatscreen(request, pk):
    information = User.objects.get(pk=pk)

    if request.method == 'POST':
        message_text = request.POST.get('message')

        if message_text:
            # Create a PersonalChat object for the sent message
            error = PersonalChat.objects.create(
                sender=request.user,
                receiver=User.objects.get(id=pk),
                message=request.POST.get('message'),
                statis="sent"
            )
            # Assuming you want to send a JSON response
            print(error)
            return JsonResponse({'status': 'success', 'message': 'Message sent successfully'})
        # return JsonResponse({'status': 'error', 'message': 'Invalid request or empty message'})
    name = information.username
    return render(request, 'socialmedia/chatare.html', {"pk": pk, 'name': name})


@login_required(login_url='login')
@csrf_exempt
def loadpersonalchats(request, pk):
    chats = PersonalChat.objects.filter(
        (Q(sender=request.user) & Q(receiver_id=pk)) | (Q(receiver=request.user) & Q(sender_id=pk))
    ).order_by('time')
    user = request.user  # Corrected the typo here
    message = [
        {
            "user": user.pk,
            # "usericon": user.avator.url,
            "senderid": mes.sender.id,
            "sender": mes.sender.username,
            "time": timesince(mes.time),
            "receiverid": mes.receiver.id,
            "receiver": mes.receiver.username,
            "message": mes.message,
            'messageid': mes.id,
            "sendericon": mes.sender.avator.url,
            "receivericon": mes.receiver.avator.url
        } for mes in chats
    ]
    return JsonResponse({"messages": message})


@login_required(login_url='login')
@csrf_exempt
def getchats(request, type):
    try:
        if type == 'individual':
            mychats = PersonalChat.objects.filter(
                Q(sender=request.user) | Q(receiver=request.user)).distinct().order_by(
                '-time')
            mychat = [
                {
                    'user': request.user.username,
                    'type': 'individual',
                    'sendername': i.sender.username,
                    'senderid': i.sender.id,
                    'receiver': i.receiver.username,
                    'receiverid': i.receiver.id,
                    'sendericon': i.sender.avator.url,
                    'message': i.message,
                    'receivericon': i.sender.avator.url,
                    'time': timesince(i.time)
                } for i in mychats
            ]

        else:
            mychats = GroupMembers.objects.filter(member=request.user).order_by('-id')

            mychat = [
                {
                    'type': 'group',
                    'groupname': i.group.name,
                    'icon': i.group.icon.url,
                    'time': timesince(i.group.created),
                    'members': GroupMembers.objects.filter(group=i.group).count(),
                    'groupid': i.group.id,
                    'code': i.group.groupcode
                } for i in mychats
            ]

        context = {'mychats': mychat}
        return JsonResponse(context)

    except Exception as e:
        # Log the exception for debugging purposes
        print(f"Error in getchats view: {e}")
        return JsonResponse({'error': 'Internal Server Error'}, status=500)


@login_required(login_url='login')
@csrf_exempt
def deletepmessage(request, pkmessage, pkroom):
    obj = PersonalChat.objects.get(pk=pkmessage)
    if request.method == 'POST':
        obj.delete()
        information = User.objects.get(pk=pkroom)
        name = information.username
        return render(request, 'socialmedia/chatare.html', {"pk": pkroom, 'name': name})

    return render(request, 'socialmedia/delete.html', {'obj': obj})


@login_required(login_url='login')
@csrf_exempt
def groupchat(request, code):
    try:
        group_member = GroupMembers.objects.get(member=request.user, group__groupcode=code)
    except ObjectDoesNotExist:
        # Handle the case where the user is not a member of the group
        return JsonResponse({'error': 'User is not a member of the group'}, status=403)

    chat = GroupMessages.objects.filter(group__groupcode=code)
    mychat = [
        {
            'user': request.user.username,
            'type': 'group',
            'sendername': message.sender.username,
            'senderid': message.sender.id,
            'sendericon': message.sender.avator.url,
            'message': message.message,
            'messageid': message.id,
            'time': timesince(message.time)
        } for message in chat
    ]

    context = {'mychats': mychat}
    return JsonResponse(context)


from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import GroupMessages, Groups


@login_required(login_url='login')
@csrf_exempt
def groupchatscreen(request, code):
    group = get_object_or_404(Groups, groupcode=code)
    try:
        member = GroupMembers.objects.get(member=request.user, group=group)
    except ObjectDoesNotExist:
        if request.method == 'POST':
            password = request.POST.get('password')
            if password:
                if group.group_password == password:
                    verified, created = GroupMembers.objects.get_or_create(
                        group=group,
                        member=request.user
                    )
                    name = group.name
                    return render(request, 'socialmedia/groupchatarea.html', {"code": code, 'name': name})
        context = {'name': group.name}
        return render(request, 'socialmedia/verify.html', context)

    if request.method == 'POST':
        message_text = request.POST.get('message')

        if message_text:
            try:
                GroupMessages.objects.create(
                    sender=request.user,
                    message=message_text,
                    group=group,
                )
                return JsonResponse({'status': 'success', 'message': 'Message sent successfully'})
            except Exception as e:
                # Handle the error, log it, or provide an appropriate response
                return JsonResponse({'status': 'error', 'message': f'Error: {str(e)}'})

        return JsonResponse({'status': 'error', 'message': 'Invalid request or empty message'})

    name = group.name
    return render(request, 'socialmedia/groupchatarea.html', {"code": code, 'name': name})


@login_required(login_url='login')
@csrf_exempt
def deletegroupmessage(request, code, pk):
    obj = GroupMessages.objects.get(pk=pk)
    information = Groups.objects.get(groupcode=code)
    if request.method == 'POST':
        obj.delete()
        name = information.name
        return render(request, 'socialmedia/groupchatarea.html', {"code": code, 'name': name})

    return render(request, 'socialmedia/delete.html', {'obj': obj})


def getusernames(request):
    usrs = User.objects.all()
    user = [{
        "name": i.username,
        "id": i.id,
    } for i in usrs]
    groups = Groups.objects.all()
    group = [{
        "name": i.name,
        "code": i.groupcode

    } for i in groups]

    return JsonResponse({"users": user, "groups": group})


@login_required(login_url='login')
@csrf_exempt
def creategroup(request):
    form = CreateGroup()
    context ={'form':form}
    return render(request, 'socialmedia/creategroup.html', context)
