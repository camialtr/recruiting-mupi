from allauth.account.adapter import DefaultAccountAdapter


class NoSignupAccountAdapter(DefaultAccountAdapter):
    """
    Adapter customizado que desabilita o cadastro de novos usuários.
    Usuários só podem ser criados via linha de comando (createsuperuser).
    """
    
    def is_open_for_signup(self, request):
        return False
