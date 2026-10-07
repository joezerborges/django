# Guia do professor: livraria Margem

Roteiro para construir com a turma o mesmo site deste projeto: uma livraria independente com página inicial, catálogo de três livros e página sobre a livraria. A aplicação usa Django para rotas e conteúdo, templates Django para o HTML e Bootstrap para a grade responsiva e navegação.

## Visão da aula

- Duração sugerida: duas aulas de 50 minutos.
- Público: alunos que já viram o básico de Python e HTML. Não é necessário conhecer Django.
- Produto final: site navegável em `/`, `/livros/` e `/sobre/`, com layout responsivo e três livros.
- Objetivos: distinguir projeto de app no Django, ligar URL a view e template, reutilizar um template-base e renderizar uma lista com `{% for %}`.

## Antes da aula

1. Abra este projeto e teste o site em `http://127.0.0.1:8000/`.
2. Deixe acessíveis o terminal integrado, o navegador e os arquivos de referência listados ao final.
3. Para a turma começar do zero, cada aluno deve usar uma pasta vazia. Não execute `startproject` sobre uma pasta que já contenha o projeto.
4. Bootstrap e as fontes são carregados por CDN; a atividade precisa de internet para reproduzir a aparência completa. As capas também vêm de um serviço externo, mas o site mostra uma capa tipográfica se uma imagem não carregar.

## Aula 1: Django e conteúdo

### 1. Preparar o ambiente (10 min)

Peça aos alunos que abram uma pasta vazia no VS Code e executem no PowerShell:

```powershell
py -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install "Django>=6.1,<6.2"
django-admin startproject livraria .
python manage.py startapp catalog
```

Explique que `venv` isola as dependências, `livraria` é a configuração do projeto Django e `catalog` é a app que contém uma parte funcional do site. A opção `.` cria o projeto na pasta atual.

**Pergunte:** “Qual comando inicia o servidor? Qual comando cria uma app?”

**Checkpoint:** `python manage.py check` deve terminar com `System check identified no issues`.

### 2. Registrar a app e configurar o idioma (5 min)

Em `livraria/settings.py`, adicionar `'catalog.apps.CatalogConfig'` em `INSTALLED_APPS`. Ajustar:

```python
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
```

Explique que registrar a app permite ao Django encontrar seus recursos. O idioma e o fuso definem opções globais do projeto.

### 3. Criar as rotas (10 min)

Em `catalog/urls.py`, criar as três rotas:

```python
from django.urls import path
from . import views

app_name = 'catalog'

urlpatterns = [
    path('', views.home, name='home'),
    path('livros/', views.books, name='books'),
    path('sobre/', views.about, name='about'),
]
```

Em `livraria/urls.py`, importar `include` e acrescentar `path('', include('catalog.urls'))` a `urlpatterns`. Mostre que a URL do projeto encaminha as requisições para a app.

**Pergunte:** “O que muda entre o endereço `/livros/` e o nome reverso `catalog:books`?”

### 4. Preparar dados e views (15 min)

Em `catalog/views.py`, criar uma lista `BOOKS` com três dicionários. Cada dicionário precisa de `title`, `author`, `isbn`, `price`, `category`, `description` e `color`. Depois, criar uma view para cada página:

```python
from django.shortcuts import render

def home(request):
    return render(request, 'catalog/home.html', {'featured_book': BOOKS[0]})

def books(request):
    return render(request, 'catalog/books.html', {'books': BOOKS})

def about(request):
    return render(request, 'catalog/about.html')
```

Use a lista completa de livros em [`catalog/views.py`](catalog/views.py) como gabarito. Explique o fluxo: URL seleciona view; view escolhe o template e envia dados no contexto; template apresenta os dados.

**Checkpoint:** a view `books` envia a lista inteira; a view `home` envia somente o primeiro livro como destaque.

### 5. Verificar o encaminhamento (10 min)

Execute:

```powershell
python manage.py check
```

Antes de abrir o navegador, convide a turma a explicar o caminho de uma requisição. Se houver erro, verifique nomes de funções, import de `include`, registro da app e caminho dos templates.

## Aula 2: templates, Bootstrap e acabamento

### 6. Montar o template compartilhado (10 min)

Criar as pastas `catalog/templates/catalog/` e `catalog/static/catalog/`. Em `base.html`, incluir estrutura HTML, links de Bootstrap e CSS, barra superior, navegação, bloco principal e rodapé. Usar `{% load static %}` para carregar o CSS.

Explique que `{% block content %}` é um espaço substituível e que as outras páginas podem herdar a navegação e o rodapé sem copiá-los.

**Pergunte:** “Se mudarmos a navegação em `base.html`, em quantas páginas precisamos fazer essa alteração?”

### 7. Criar as três páginas (20 min)

Cada arquivo começa com `{% extends 'catalog/base.html' %}` e preenche o bloco `content`:

1. `home.html`: chamada principal, link para o catálogo e imagem do livro em destaque. O dado chega como `featured_book`.
2. `books.html`: catálogo em grade Bootstrap. Usar `{% for book in books %}` para criar um cartão por livro e `{{ book.title }}` para apresentar valores.
3. `about.html`: texto sobre a livraria e link para o catálogo.

Projete os arquivos [`home.html`](catalog/templates/catalog/home.html), [`books.html`](catalog/templates/catalog/books.html) e [`about.html`](catalog/templates/catalog/about.html) como gabarito. Primeiro peça aos alunos para identificar quais classes Bootstrap cuidam da grade (`container`, `row`, `col-*`) e quais classes próprias estão estilizadas no CSS.

**Checkpoint:** acessar `/`, `/livros/` e `/sobre/` não pode gerar erro 404 ou `TemplateDoesNotExist`. O catálogo deve mostrar exatamente três cartões.

### 8. Aplicar o visual e testar (15 min)

Criar `catalog/static/catalog/store.css`. Para reproduzir este visual, usar o arquivo [`store.css`](catalog/static/catalog/store.css) como referência: paleta clara com laranja, azul e verde, títulos serifados, capas coloridas e ajustes para telas estreitas. O Bootstrap fornece a estrutura; as classes próprias dão a identidade da Margem.

Explique a diferença entre CSS de framework e CSS do projeto. Mostre também o `onerror` das capas: se a imagem externa falhar, a página revela a alternativa tipográfica.

Rodar a aplicação:

```powershell
python manage.py migrate
python manage.py runserver
```

Abrir `http://127.0.0.1:8000/`, navegar pelas três páginas, reduzir a largura do navegador e observar o menu e o catálogo. Encerrar a atividade com:

```powershell
python manage.py test catalog
```

Os testes em [`catalog/tests.py`](catalog/tests.py) verificam se as três rotas respondem e se o catálogo contém os três títulos.

## Dúvidas comuns

| Sintoma | O que revisar com a turma |
| --- | --- |
| `No module named django` | O ambiente virtual está ativado? Django foi instalado nele? |
| Erro 404 numa página | O caminho foi declarado em `catalog/urls.py` e a app foi incluída nas URLs do projeto? |
| `TemplateDoesNotExist` | O arquivo está em `catalog/templates/catalog/` e o nome passado a `render` coincide com o caminho? |
| CSS não aparece | O template tem `{% load static %}` e o caminho corresponde a `catalog/static/catalog/store.css`? |
| Imagem de capa ausente | O serviço externo pode estar indisponível; verificar se a capa tipográfica aparece. |
| Porta 8000 ocupada | Parar o outro servidor ou executar `python manage.py runserver 8001`. |

## Encerramento e avaliação

Peça a cada aluno que explique uma rota completa (URL → view → template) e que altere um detalhe simples, como o texto da chamada principal ou a descrição de um livro. Considere a atividade concluída quando as três páginas carregarem, os três cartões forem gerados pelo loop e a navegação funcionar em tela estreita.

## Arquivos de referência

- Dados e views: [`catalog/views.py`](catalog/views.py)
- Rotas da app: [`catalog/urls.py`](catalog/urls.py)
- Rotas do projeto: [`livraria/urls.py`](livraria/urls.py)
- Navegação compartilhada: [`base.html`](catalog/templates/catalog/base.html)
- Páginas: [`home.html`](catalog/templates/catalog/home.html), [`books.html`](catalog/templates/catalog/books.html), [`about.html`](catalog/templates/catalog/about.html)
- Estilo e testes: [`store.css`](catalog/static/catalog/store.css), [`tests.py`](catalog/tests.py)