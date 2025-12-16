from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .forms import MessageForm, MessageUpdateForm
from .models import Message


class LoginViewCustom(LoginView):
	template_name = 'login.html'


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
	if not msg.read:
		msg.mark_as_read()
	return render(request, 'message_detail.html', {'message_obj': msg})


@login_required
def message_edit(request, pk: int):
	msg = get_object_or_404(Message, pk=pk)
	if request.method == 'POST':
		form = MessageUpdateForm(request.POST, instance=msg)
		if form.is_valid():
			form.save()
			messages.success(request, 'Mensagem atualizada.')
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
		return redirect('messages_list')
	return render(request, 'message_delete_confirm.html', {'message_obj': msg})


@login_required
def logout_confirm(request):
	if request.method == 'POST':
		logout(request)
		messages.info(request, 'Você saiu da área administrativa.')
		return redirect('landpage')
	return render(request, 'logout_confirm.html')
