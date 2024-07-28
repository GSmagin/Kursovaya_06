from django.shortcuts import render


def index(request):
    return render(request, 'main/index.html')


def contacts(request):
    return render(request, 'main/contacts.html')


def not_found(request):
    return render(request, 'main/not_found.html')

