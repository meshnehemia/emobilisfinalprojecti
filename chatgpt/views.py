from django.contrib.auth.decorators import login_required
from django.db.models import Q
from openai import OpenAI
from django.shortcuts import render
from django.http import JsonResponse
from openai import AsyncOpenAI
from socialmedia import views
from socialmedia.models import Message, Topic, Room

openai_api_key = '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'


@login_required(login_url='login')
def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )
    topics = Topic.objects.all()[0:5]
    room_count = rooms.count()
    user = request.user
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))
    context = {'rooms': rooms, 'topics': topics, 'room_count': room_count, "room_messages": room_messages, 'user': user}
    if request.method == 'POST':
        message = request.POST.get('message')
        response = ask_openai(message)
        return JsonResponse({'message': message, 'response': response})
    return render(request, 'chatgpt/chatbot.html', context)


def ask_openai(message):
    conversation = [
        {"role": "system", "content": "You are a intelligent."},
        {"role": "user", "content": message}
    ]
    client = OpenAI(
        api_key=openai_api_key  # this is also the default, it can be omitted
    )
    # client = AsyncOpenAI()
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=conversation
    )
    answer = response.choices[0].message.content
    return answer
