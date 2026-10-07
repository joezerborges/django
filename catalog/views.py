from django.shortcuts import render

BOOKS = [
    {
        'title': 'Torto Arado',
        'author': 'Itamar Vieira Junior',
        'isbn': '9786580309313',
        'price': 'R$ 54,90',
        'category': 'Literatura brasileira',
        'description': 'Duas irmãs, uma fazenda no sertão baiano e uma história sobre terra, memória e pertencimento.',
        'color': 'clay',
    },
    {
        'title': 'A Hora da Estrela',
        'author': 'Clarice Lispector',
        'isbn': '9788520925692',
        'price': 'R$ 39,90',
        'category': 'Clássicos brasileiros',
        'description': 'A vida de Macabéa ganha voz numa narrativa delicada e inquieta sobre existir e ser visto.',
        'color': 'blue',
    },
    {
        'title': 'O Pequeno Príncipe',
        'author': 'Antoine de Saint-Exupéry',
        'isbn': '9780156012195',
        'price': 'R$ 44,90',
        'category': 'Fábula',
        'description': 'Uma viagem entre planetas que transforma amizade, cuidado e imaginação em descobertas.',
        'color': 'yellow',
    },
]


def home(request):
    return render(request, 'catalog/home.html', {'featured_book': BOOKS[0]})


def books(request):
    return render(request, 'catalog/books.html', {'books': BOOKS})


def about(request):
    return render(request, 'catalog/about.html')
