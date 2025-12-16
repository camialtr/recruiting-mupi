from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.db.models import Count, Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .forms import MessageForm, MessageUpdateForm
from .models import Message


class LoginViewCustom(LoginView):
	template_name = 'login.html'


@login_required
def dashboard(request):
	search_query = request.GET.get('search', '')
	status_filter = request.GET.get('status', '')
	
	messages_qs = Message.objects.all()
	
	if search_query:
		messages_qs = messages_qs.filter(
			Q(name__icontains=search_query) |
			Q(email__icontains=search_query) |
			Q(message__icontains=search_query)
		)
	
	if status_filter == 'read':
		messages_qs = messages_qs.filter(read=True)
	elif status_filter == 'unread':
		messages_qs = messages_qs.filter(read=False)
	
	total_messages = Message.objects.count()
	unread_messages = Message.objects.filter(read=False).count()
	read_messages = Message.objects.filter(read=True).count()

	context = {
		'total_messages': total_messages,
		'unread_messages': unread_messages,
		'read_messages': read_messages,
		'messages': messages_qs,
		'search_query': search_query,
		'status_filter': status_filter,
	}
	
	if request.headers.get('HX-Request'):
		return render(request, 'messages_table.html', context)
	
	return render(request, 'dashboard.html', context)


@login_required
def dashboard_stats(request):
	total_messages = Message.objects.count()
	unread_messages = Message.objects.filter(read=False).count()
	read_messages = Message.objects.filter(read=True).count()

	context = {
		'total_messages': total_messages,
		'unread_messages': unread_messages,
		'read_messages': read_messages,
	}
	
	return render(request, 'dashboard.html', context)


def landpage(request):
	if request.method == 'POST':
		form = MessageForm(request.POST)
		if form.is_valid():
			form.save()
			messages.success(request, 'Mensagem enviada com sucesso!')
			return redirect('landpage')
	else:
		form = MessageForm()
	return render(request, 'landpage.html', {'form': form})


@login_required
def messages_list(request):
	msgs = Message.objects.all()
	return render(request, 'messages_list.html', {'messages_list': msgs})


@login_required
def message_detail(request, pk: int):
	msg = get_object_or_404(Message, pk=pk)
	was_unread = not msg.read
	if was_unread:
		msg.mark_as_read()
	
	if request.headers.get('HX-Request'):
		response = render(request, 'message_detail.html', {'message_obj': msg})
		if was_unread:
			response['HX-Trigger'] = 'refresh-stats'
		return response
	return render(request, 'message_detail.html', {'message_obj': msg})


@login_required
def message_edit(request, pk: int):
	msg = get_object_or_404(Message, pk=pk)
	if request.method == 'POST':
		form = MessageUpdateForm(request.POST, instance=msg)
		if form.is_valid():
			form.save()
			messages.success(request, 'Mensagem atualizada.')
			if request.headers.get('HX-Request'):
				return HttpResponse(status=204, headers={'HX-Trigger': 'modal-close, refresh-messages'})
			return redirect('message_detail', pk=msg.pk)
	else:
		form = MessageUpdateForm(instance=msg)
	return render(request, 'message_edit.html', {'form': form, 'message_obj': msg})


@login_required
def message_delete_confirm(request, pk: int):
	msg = get_object_or_404(Message, pk=pk)
	if request.method == 'POST':
		msg.delete()
		messages.success(request, 'Mensagem excluída.')
		if request.headers.get('HX-Request'):
			return HttpResponse(status=204, headers={'HX-Trigger': 'modal-close, refresh-messages'})
		return redirect('messages_list')
	return render(request, 'message_delete_confirm.html', {'message_obj': msg})


@login_required
def toggle_message_read(request, pk: int):
	msg = get_object_or_404(Message, pk=pk)
	msg.read = not msg.read
	msg.save(update_fields=['read'])
	
	if request.headers.get('HX-Request'):
		status_text = "Sim" if msg.read else "Não"
		html = f'<span id="read-text-{msg.pk}" class="read-status">{status_text}</span>'
		return HttpResponse(html, headers={'HX-Trigger': 'refresh-stats'})
	return redirect('admin')


@login_required
def logout_confirm(request):
	if request.method == 'POST':
		logout(request)
		messages.info(request, 'Você saiu da área administrativa.')
		if request.headers.get('HX-Request'):
			return HttpResponse(status=204, headers={'HX-Redirect': '/'})
		return redirect('landpage')
	
	is_htmx = request.headers.get('HX-Request')
	return render(request, 'logout_confirm.html', {'is_htmx': is_htmx})
