import json

from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q, Count
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST, require_http_methods

from .forms import MessageForm, MessageUpdateForm, CreateUserForm, ChangeUserPasswordForm
from .models import Message, AuditLog


def dev_required(view_func):
    """Decorator que verifica se o usuário é dev (superuser)"""
    def wrapper(request, *args, **kwargs):
        if not request.user.is_superuser:
            if request.headers.get('HX-Request'):
                return HttpResponseForbidden('Acesso negado')
            return redirect('admin')
        return view_func(request, *args, **kwargs)
    return wrapper


def redirect_to_admin(request):
    return redirect('admin')


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
    
    counts = Message.objects.aggregate(
        total=Count('id'),
        unread=Count('id', filter=Q(read=False)),
        read=Count('id', filter=Q(read=True)),
    )
    total_messages = counts['total']
    unread_messages = counts['unread']
    read_messages = counts['read']
    
    # Verifica se o usuário é dev (superuser)
    is_dev = request.user.is_superuser
    
    # Lista de usuários ativos (apenas para devs)
    active_users = []
    audit_logs = []
    if is_dev:
        active_users = User.objects.all()
        audit_logs = AuditLog.objects.all()[:50]

    context = {
        'total_messages': total_messages,
        'unread_messages': unread_messages,
        'read_messages': read_messages,
        'message_list': messages_qs,
        'search_query': search_query,
        'status_filter': status_filter,
        'is_dev': is_dev,
        'active_users': active_users,
        'audit_logs': audit_logs,
    }
    
    # Se é HTMX, verifica se quer seção específica
    if request.headers.get('HX-Request'):
        section = request.GET.get('section')
        if section == 'users' or section == 'audit':
            return render(request, 'messages_list.html', context)
        return render(request, 'messages_table.html', context)
    
    return render(request, 'messages_list.html', context)


@login_required
def dashboard_stats(request):
    counts = Message.objects.aggregate(
        total=Count('id'),
        unread=Count('id', filter=Q(read=False)),
        read=Count('id', filter=Q(read=True)),
    )
    total_messages = counts['total']
    unread_messages = counts['unread']
    read_messages = counts['read']
    
    is_dev = request.user.is_superuser
    active_users = []
    audit_logs = []
    messages_qs = Message.objects.all()
    if is_dev:
        active_users = User.objects.all()
        audit_logs = AuditLog.objects.all()[:50]

    context = {
        'total_messages': total_messages,
        'unread_messages': unread_messages,
        'read_messages': read_messages,
        'is_dev': is_dev,
        'active_users': active_users,
        'audit_logs': audit_logs,
        'message_list': messages_qs,
        'search_query': '',
        'status_filter': '',
    }
    
    return render(request, 'messages_list.html', context)


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
def message_detail(request, pk: int):
    if not request.headers.get('HX-Request'):
        return redirect('admin')
    
    msg = get_object_or_404(Message, pk=pk)
    was_unread = not msg.read
    if was_unread:
        msg.mark_as_read()
    
    is_dev = request.user.is_superuser
    response = render(request, 'message_detail.html', {'message_obj': msg, 'is_dev': is_dev})
    if was_unread:
        response['HX-Trigger'] = 'refresh-stats, refresh-messages'
    return response


@login_required
@require_http_methods(["GET", "POST"])
@dev_required
def message_edit(request, pk: int):
    if not request.headers.get('HX-Request'):
        return redirect('admin')
    
    msg = get_object_or_404(Message, pk=pk)
    if request.method == 'POST':
        form = MessageUpdateForm(request.POST, instance=msg)
        if form.is_valid():
            form.save()
            AuditLog.log(request.user, 'edit', f'Editou a mensagem de {msg.name}.')
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        'modal-close': True,
                        'refresh-messages': True,
                        'refresh-audit': True,
                        'toast-add': {'level': 'success', 'message': 'Mensagem atualizada.'},
                    })
                },
            )
    else:
        form = MessageUpdateForm(instance=msg)
    return render(request, 'message_edit.html', {'form': form, 'message_obj': msg})


@login_required
@require_http_methods(["GET", "POST"])
@dev_required
def message_delete_confirm(request, pk: int):
    if not request.headers.get('HX-Request'):
        return redirect('admin')
    
    msg = get_object_or_404(Message, pk=pk)
    if request.method == 'POST':
        msg_name = msg.name
        msg.delete()
        AuditLog.log(request.user, 'delete', f'Excluiu a mensagem de {msg_name}.')
        return HttpResponse(
            status=204,
            headers={
                'HX-Trigger': json.dumps({
                    'modal-close': True,
                    'refresh-messages': True,
                    'refresh-audit': True,
                    'toast-add': {'level': 'success', 'message': 'Mensagem excluída.'},
                })
            },
        )
    return render(request, 'message_delete_confirm.html', {'message_obj': msg})


@login_required
@require_POST
def toggle_message_read(request, pk: int):
    if not request.headers.get('HX-Request'):
        return redirect('admin')
    
    msg = get_object_or_404(Message, pk=pk)
    msg.read = not msg.read
    msg.save(update_fields=['read'])
    
    if msg.read:
        AuditLog.log(request.user, 'view', f'Marcou como lida a mensagem de {msg.name}.')
        css_class = "px-2 py-1 rounded-full text-xs font-semibold border bg-accent/20 text-accent-dark border-accent-dark/30"
    else:
        AuditLog.log(request.user, 'unview', f'Marcou como não lida a mensagem de {msg.name}.')
        css_class = "px-2 py-1 rounded-full text-xs font-semibold border bg-accent-ice/20 text-accent-ice-dark border-accent-ice-dark/30"
    
    status_text = "Sim" if msg.read else "Não"
    html = f'<span id="read-text-{msg.pk}" class="{css_class}">{status_text}</span>'
    return HttpResponse(html, headers={'HX-Trigger': 'refresh-stats, refresh-messages, refresh-audit'})


@login_required
@require_http_methods(["GET", "POST"])
def logout_confirm(request):
    if not request.headers.get('HX-Request'):
        return redirect('admin')
    
    if request.method == 'POST':
        logout(request)
        return HttpResponse(status=204, headers={'HX-Redirect': '/'})
    
    return render(request, 'logout_confirm.html')


# === Views de gerenciamento de usuários (apenas devs) ===

@login_required
@require_http_methods(["GET", "POST"])
@dev_required
def user_create(request):
    if not request.headers.get('HX-Request'):
        return redirect('admin')
    
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            AuditLog.log(request.user, 'create_user', f'Criou o usuário {new_user.username}.')
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        'modal-close': True,
                        'refresh-users': True,
                        'refresh-audit': True,
                        'toast-add': {'level': 'success', 'message': 'Usuário criado com sucesso.'},
                    })
                },
            )
    else:
        form = CreateUserForm()
    return render(request, 'user_create.html', {'form': form})


@login_required
@require_http_methods(["GET", "POST"])
@dev_required
def user_change_password(request, pk: int):
    if not request.headers.get('HX-Request'):
        return redirect('admin')
    
    target_user = get_object_or_404(User, pk=pk)
    
    if request.method == 'POST':
        form = ChangeUserPasswordForm(target_user, request.POST)
        if form.is_valid():
            form.save()
            AuditLog.log(request.user, 'change_password', f'Alterou a senha de {target_user.username}.')
            success_msg = f'Senha do usuário {target_user.username} alterada.'
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        'modal-close': True,
                        'refresh-audit': True,
                        'toast-add': {'level': 'success', 'message': success_msg},
                    })
                },
            )
    else:
        form = ChangeUserPasswordForm(target_user)
    return render(request, 'user_change_password.html', {'form': form, 'target_user': target_user})


@login_required
@require_http_methods(["GET", "POST"])
@dev_required
def user_delete(request, pk: int):
    if not request.headers.get('HX-Request'):
        return redirect('admin')
    
    target_user = get_object_or_404(User, pk=pk)
    
    # Não pode deletar a si mesmo
    if target_user == request.user:
        return HttpResponseForbidden('Você não pode excluir sua própria conta.')
    
    if request.method == 'POST':
        username = target_user.username
        target_user.delete()
        AuditLog.log(request.user, 'delete_user', f'Excluiu o usuário {username}.')
        return HttpResponse(
            status=204,
            headers={
                'HX-Trigger': json.dumps({
                    'modal-close': True,
                    'refresh-users': True,
                    'refresh-audit': True,
                    'toast-add': {'level': 'success', 'message': f'Usuário {username} excluído.'},
                })
            },
        )
    
    return render(request, 'user_delete_confirm.html', {'target_user': target_user})


def password_reset_modal(request):
    if not request.headers.get('HX-Request'):
        return redirect('admin')
    return render(request, 'account/password_reset_modal.html')


def signup_modal(request):
    if not request.headers.get('HX-Request'):
        return redirect('admin')
    return render(request, 'account/signup_modal.html')
