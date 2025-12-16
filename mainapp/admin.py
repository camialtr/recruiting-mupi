from django.contrib import admin
from .models import Message


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
	list_display = ('id', 'name', 'email', 'read', 'sent_at')
	list_filter = ('read', 'sent_at')
	search_fields = ('name', 'email', 'message')
	ordering = ('-sent_at',)
