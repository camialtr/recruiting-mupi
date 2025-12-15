<img src="logo.png" alt="Mupi Systems Logo" width="200"/>

# 🚀 Teste Técnico - Desenvolvedor Jr. Full Stack

---

## 🎯 Objetivos

- Desenvolver uma **landpage atraente** com formulário de contato funcional
- Criar uma **área administrativa protegida** para gerenciamento de mensagens
- Demonstrar habilidades em **UI/UX design** com foco em estética e usabilidade
- Aplicar boas práticas de desenvolvimento **Django** e **frontend moderno**
- Implementar interatividade usando **HTMX** e **Alpine.js**

---

## 📋 Instruções

### 🔀 Fork do Repositório

1. Faça um **fork** deste repositório para sua conta pessoal do GitHub
2. Trabalhe em seu próprio fork

### 💻 Implementação

- Desenvolva o projeto conforme os requisitos abaixo
- Use **Django**, **Django Templates**, **TailwindCSS**, **HTMX** e **Alpine.js** conforme apropriado

### 📤 Submissão

1. Após finalizar, abra um **Pull Request** do seu fork para o repositório original
2. Aguarde o agendamento da reunião para avaliação do teste

### 📝 Documentação

Inclua um arquivo `README.md` com:
- ✅ Descrição do projeto
- ✅ Passo a passo para rodar a aplicação
- ✅ Decisões técnicas importantes

---

## 🛠️ Requisitos Técnicos Mínimos

### 🐍 Backend (Django)

| Requisito | Descrição |
|-----------|-----------|
| **Versão** | Django 3.2+ |
| **Templates Obrigatórios** | `landpage.html` - Página inicial com formulário<br>`login.html` - Tela de login personalizada<br>`messages_list.html` - Listagem de mensagens<br>`message_detail.html` - Visualização individual de mensagem<br>`message_edit.html` - Formulário de edição de mensagem (ou modal)<br>`message_delete_confirm.html` - Confirmação de exclusão (ou modal)<br>`logout_confirm.html` - Confirmação de logout (ou modal) |
| **Model** | Mensagem com campos: `nome`, `email`, `mensagem`, `data_envio`, `lido` (boolean) |
| **Autenticação** | Sistema de autenticação para área administrativa |
| **CRUD de Mensagens** | Admin deve poder visualizar, editar e apagar mensagens |
| **API** | Endpoint para receber mensagens do formulário |

### 🎨 Frontend

#### Tecnologias Obrigatórias

- **TailwindCSS** - Para estilização (obrigatório)
- **HTMX** - Para interações assíncronas (pelo menos uma implementação)
- **Alpine.js** - Para interatividade (pelo menos uma implementação)

#### Requisitos de Interface

- Design **responsivo**
- Formulário **funcional** na landpage
- Tabela/listagem de mensagens na área admin

### 🧹 Qualidade de Código

- Versionamento com **commits semânticos**
- Estrutura de projeto Django **organizada**
- Código **limpo** e bem documentado
- Arquivos estáticos organizados

---

## 🎨 Critérios de Avaliação

### UI/UX Design
- Estética visual atraente
- Experiência de usuário intuitiva
- Consistência visual
- Responsividade

### Qualidade de Código
- Organização do projeto
- Clareza e legibilidade
- Boas práticas Django
- Separação de responsabilidades

### Funcionalidade
- Todos os requisitos mínimos atendidos
- Funcionamento correto das features
- Tratamento de erros

### Versionamento
- Commits descritivos e organizados
- Estrutura de branches (se aplicável)
- Mensagens de commit claras

### Uso das Tecnologias
- Aplicação apropriada de HTMX e Alpine.js
- Eficiência no uso do Tailwind
- Decisões técnicas justificadas

---

## ✨ Diferenciais

Os seguintes elementos serão considerados **pontos extras** na avaliação:

### Design e UX
- 🎨 **Fontes personalizadas** - Uso de tipografia além das fontes padrão do sistema
- 🌗 **Contraste bem trabalhado** - Bom uso de cores, contraste adequado para acessibilidade
- 🎭 **Identidade visual consistente** - Paleta de cores coesa, elementos visuais harmônicos
- ⚡ **Animações e transições suaves** - Microinterações que melhoram a experiência
- 📱 **Design mobile-first** - Experiência otimizada para dispositivos móveis

### Funcionalidades Avançadas com HTMX e Alpine.js
- 🔔 **Modais para confirmações** - Implementar logout, edição e exclusão de mensagens via modal usando HTMX/Alpine.js
- ✏️ **Edição inline** - Editar mensagens diretamente na listagem sem recarregar a página
- 🗑️ **Exclusão com confirmação dinâmica** - Modal de confirmação antes de apagar, com feedback visual
- 🔄 **Marcar como lida sem reload** - Alternar status de mensagem usando HTMX
- 🔍 **Busca e filtros avançados** - Sistema de busca por texto, filtros por data ou status com HTMX
- 📊 **Dashboard com estatísticas** - Quantidade de mensagens lidas/não lidas, gráficos dinâmicos

---

## 💡 Diretrizes Criativas

### 🌐 Landpage

> **Liberdade total!** Escolha qualquer produto/serviço de sua preferência (pode ser real ou fictício)

**Exemplos na pasta `/examples`** (boas referências de design)

#### Elementos Essenciais

| Seção | Descrição |
|-------|-----------|
| **Header** | Menu de navegação |
| **Hero Section** | Banner principal chamativo |
| **Features/Benefícios** | Destaques do produto/serviço |
| **Formulário de Contato** | Form funcional e validado |
| **Footer** | Informações de rodapé |

### 🔐 Área Administrativa

#### Funcionamento

A área administrativa é uma **seção protegida** que requer autenticação. O fluxo funciona da seguinte forma:

1. **Criação de Usuário Administrador**
   - Durante a configuração inicial, você deve criar um superusuário usando `python manage.py createsuperuser`
   - Este usuário terá acesso à área administrativa

2. **Sistema de Login**
   - Implemente uma **página de login personalizada** (não usar o admin padrão do Django)
   - Design deve seguir a identidade visual do projeto
   - Apenas usuários autenticados podem acessar a área de visualização de mensagens
   - Use o sistema de autenticação nativo do Django (`django.contrib.auth`)

3. **Proteção de Rotas**
   - Use decorators como `@login_required` para proteger as views administrativas
   - Redirecione usuários não autenticados para a página de login

#### Telas Obrigatórias

| Tela | Descrição |
|------|-----------|
| **Landpage** | Página pública com formulário de contato funcional |
| **Login** | Tela personalizada para autenticação do admin |
| **Listagem de Mensagens** | Exibe todas as mensagens com indicador de lidas/não lidas |
| **Visualização Individual** | Detalhes completos de uma mensagem específica |
| **Edição de Mensagem** | Formulário para editar dados de uma mensagem (ou modal) |
| **Confirmação de Exclusão** | Página de confirmação antes de apagar mensagem (ou modal) |
| **Confirmação de Logout** | Página de confirmação antes de deslogar (ou modal) |

#### Funcionalidades de Gerenciamento

O admin deve ser capaz de:

- ✅ **Visualizar** todas as mensagens em uma lista
- ✅ **Abrir** mensagens individuais para ver detalhes completos
- ✅ **Editar** mensagens (corrigir dados, adicionar notas)
- ✅ **Apagar** mensagens
- ✅ **Marcar como lida/não lida**
- ✅ **Fazer logout** com confirmação

#### Características da Interface

- Design **clean** e funcional
- **Indicador visual** de mensagens lidas/não lidas (ex: badge, cor diferente, ícone)
- **Ações rápidas** na listagem (apagar, marcar como lida)
- **Filtros opcionais**: por status (lida/não lida), por data
- **Responsividade** em todas as telas administrativas

#### Exemplo de Fluxo Completo
```
Visitante → Preenche formulário na landpage → Mensagem salva no banco

Admin → Acessa /login → Preenche credenciais → Redireciona para lista de mensagens

Admin → Visualiza lista → Clica em mensagem → Vê detalhes completos

Admin → Clica em "Editar" → Abre tela/modal de edição → Salva alterações → Retorna

Admin → Clica em "Apagar" → Confirma exclusão → Mensagem deletada → Retorna à lista

Admin → Clica em logout → Confirma logout → Deslogado
```

---

## 📁 Estrutura Esperada

```text
seu-projeto/
├── README.md
├── requirements.txt
├── manage.py
├── core/
│   ├── settings.py
│   └── urls.py
├── app_principal/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── templates/
│       ├── base.html
│       ├── landpage.html
│       ├── login.html
│       ├── logout_confirm.html
│       ├── messages_list.html
│       ├── message_detail.html
│       ├── message_edit.html
│       └── message_delete_confirm.html
├── static/
│   ├── css/
│   ├── js/
│   └── images/
├── media/
└── examples/
    └── (referências visuais)
```

---
## 🚀 Como Rodar a Aplicação (Template para seu README)

> **💡 Dica:** No seu README.md, inclua uma seção similar a esta:

### � Instalação e Execução

#### 1️⃣ Clone o repositório
```bash
git clone https://github.com/seu-usuario/seu-projeto.git
cd seu-projeto
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

---
## 📝 Notas Importantes

| Aspecto | Observação |
|-----------|--------------|
| **Liberdade Criativa** | Você tem total liberdade para escolher o tema da landpage |
| **Exemplos** | Consulte a pasta `/examples` para inspiração em design |
| **Foco** | Apesar de ser full stack, **valorizamos muito** as habilidades de UI/UX |
| **Performance** | Considere a experiência do usuário final |
| **Acessibilidade** | Boas práticas de acessibilidade são um **diferencial** |

---

<div align="center">

### Boa sorte com o teste técnico! 🌟

**Mostre suas habilidades e criatividade!**

</div>

