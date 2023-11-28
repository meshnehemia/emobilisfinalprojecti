from django.contrib import admin
from .models import Room, Topic, Message, User, PersonalChat, Groups, GroupMembers, GroupMessages, GroupAdmin

# Register your models here.
admin.site.register(User)
admin.site.register(Room)
admin.site.register(Message)
admin.site.register(Topic)
admin.site.register(PersonalChat)
admin.site.register(Groups)
admin.site.register(GroupMembers)
admin.site.register(GroupAdmin)
admin.site.register(GroupMessages)
