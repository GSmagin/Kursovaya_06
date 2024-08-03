from django.shortcuts import render


def index(request):
    # return render(request, 'main/index.html')
    page_title = 'Главная страница'
    page_description = 'Сайт где вы можете создавать, планировать свои рассылки клиентам'
    context = {
        'title': page_title,
        'description': page_description,
    }
    return render(request, 'main/index.html', context)


def contacts(request):
    return render(request, 'main/contacts.html')


def not_found(request):
    return render(request, 'main/not_found.html')

