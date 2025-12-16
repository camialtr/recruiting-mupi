from django import forms
from .models import Message

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['name', 'email', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Seu nome'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'seu@email.com'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Escreva sua mensagem'}),
        }

class MessageUpdateForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['name', 'email', 'message', 'read']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 6}),
            'read': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
