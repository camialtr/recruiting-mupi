# LP - Dance Studio - Teste Técnico

## Visão Geral

O projeto consiste da implementação da landing page de um SaaS de desenvolvimentos de timelines/mapas para Just Dance. A LP contem um formulário de contato, especificando e-mail, nome e mensagem para enviar para para os desenvolvedores. Os dados dos formulários são recebidos em uma dashboard, onde existem 2 tipos de usuarios: Devs e Viewers.

Os Devs possuem acesso completo ao gerenciamento das mensagens (incluindo exclusão e edição), gerenciamento de usuários, e visão dos logs de auditoria do sistema. Usuários do tipo Dev só podem ser criados por meio da linha de comando do Django. Já os Viewers, podem ser considerados meros moderadores. Apenas podem visualizar as mensagens ou marca-las como lidas/não lidas.

Há uma tela de login para a area administrativa, cujo acesso pode ser liberado através da landing page ao clicar 3 vezes na badge "A Nova Era do Just Dance" (libera o botão entrar), ou através da url direta. A tela de login possui informativos sobre a lógica de criação de usuários, redefinição de senha e derivados.

As tecnologias implementadas no backend cumprem os requisitos minimos, com o + da implementação do Allauth e sistema de auditoria/gerenciamento de usuários, com modelos extras. Já o front-end, utiliza as tecnologias estabelecidas para implementar interatividade/reatividade, estilos e etc...

## A Estrutura do Projeto

- `core/` : raiz do projeto django.
  - `core/wsgi.py` e `core/asgi.py` : Endpoints WSGI/ASGI, para uso servidores de produção (gunicorn/uvicorn). Esses sistemas controlam os padrões que definem como servidores web se comunicam com o app python. Não é utilizado no contexto do projeto.
  - `core/settings.py` : Configurações gerais do Django, como apps, middlewares, timezone, templates, auth, estáticos, variaveis de ambiente e integrações (como allauth).
  - `core/urls.py` : Roteamento as urls do mainapp, allauth e estáticos (debug).
- `mainapp/` : raiz do app principal (front-end).
  - `mainapp/templates` : Contem os arquivos HTML do projeto.
  - `mainapp/apps.py` : Registra o app.
  - `mainapp/models.py` : Definição e tratamento do modelo de banco de dados.
  - `mainapp/forms.py` : Definição dos formulários do Django. Com controle de validação no servidor antes de salvar os dados no DB.
  - `mainapp/admin.py` : Registra os Models (DB) do app no painel administrativo do Django. No contexto do projeto, ele remove o app admin padrão para implementação de um customizado.
  - `mainapp/adapters.py` : Arquivo de configuração de adaptações na autenticação de acordo com necessidade. Neste caso, configurado para allauth para restringir criação de usuários DEV a linha de comando.
  - `mainapp/urls.py` : Arquivo que mapeia as rotas de URL do aplicativo, responsável por redirecionar o user para os componentes/templates/views corretos.
  - `mainapp/views.py` : Contem a lógica do app. Funções e classes que processam as requisições HTTP e retornam respostas (HTML, JSON, redirecionamentos, etc).
  - `mainapp/tests.py` : Arquivo placeholder (no contexto do projeto), usado para implementação de testes automatizados. Não é utilizado neste contexto.
- `media/` : Assets enviados por usuários. Não utilizado no contexto do projeto.
- `static/` : assets estáticos (CSS, JS, fontes).
- `manage.py` : Arquivo de gerenciamento do projeto Django. Roda o servidor, cria superuser, etc...

# Decisões Técnicas

Optei por Django 6 com allauth para ter um maior controle do login, mais estável e previsível.
Bloqueei o cadastro público para evitar ruído e restringi a criação de perfis a linha de comando.
Os papéis são claros: Dev (superuser) e Viewer, sem permissões ambíguas.
`login_required` em rotas sensíveis garante sessão ativa.

Quando a ação é crítica, o sistema exige permissão de Dev via `dev_required`.
Esse decorator retorna 403 (não autorizado) quando chamado via HTMX, e redireciona para /admin ou pra LP quando acessado fora de HTMX (como na URL navegador). Fiz isso para que o HTML dos modais "componentizados" não sejam acessíveis diretamente por URL (como se fossem paginas separadas), além de manter consistentes e as URLs seguras.

Centralizei o contexto do dashboard em `get_dashboard_context` porque preciso de um ponto único de verdade para contadores, filtro e dados auxiliares. Isso reduz duplicidade e mantém as telas coerentes. Uso `aggregate` para total/lidas/não lidas direto no banco, deixando os contadores globais no topo pela estabilidade visual e aplicando o filtro apenas na tabela.

Para dados auxiliares, carrego só o necessário: usuários ativos com `only('username','is_superuser')` e logs com `select_related('user')` para não cair em N+1. Nos detalhes da mensagem eu marco leitura ao abrir o modal, porque é nessa inspeção que a leitura acontece. Isso aciona os triggers/gatilhos corretos e mantém as métricas atualizadas.

No toggle manual, eu uso os métodos do modelo (`mark_as_read`/`mark_as_unread`) para centralizar regras e evitar duplicação.

Na navegação, `/messages/` redireciona direto para o dashboard; eu removi views-pontes para simplificar e reduzir manutenção.

No front, injetei CSRF nas requisições HTMX globalmente como prevenção de requests de sites maliciosos, apesar de não ser necessário no contexto do projeto. Em layout, chamo o fragmentos do HTML pelo HTMX para reduzir FOUC (glitch ao carregar CSS) e manter a interatividade. HTML/CSS seguem responsividade sem sacrificar legibilidade.

No fim, o objetivo geral é claro: previsibilidade nos fluxos, auditoria das ações e segurança de acesso, sem abrir mão da fluidez da interface. O uso de IA foi feito principalmente para o Q&A, depuração do código e refatoração, garantindo que as soluções apresentadas fossem otimizadas o suficiente para o contexto do projeto atual.

## 🚀 Como Rodar a Aplicação (Template para seu README)

#### 1️⃣ Clone o repositório
```bash
git clone https://github.com/camialtr/recruiting-mupi.git
cd recruiting-mupi
```

#### 2️⃣ Crie e ative um ambiente virtual
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

#### 3️⃣ Instale as dependências
```bash
pip install -r requirements.txt
```

#### 4️⃣ Configure o banco de dados
```bash
python manage.py migrate
```

#### 5️⃣ Crie um superusuário
```bash
python manage.py createsuperuser
```

#### 6️⃣ Execute o servidor
```bash
python manage.py runserver
```

#### 7️⃣ Acesse a aplicação

| Página | URL |
|--------|-----|
| **Landpage** | http://localhost:8000 |
| **Área Admin** | http://localhost:8000/admin |
