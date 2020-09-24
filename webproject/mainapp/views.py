from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'mainapp/index.html')

def generic(request):
    return render(request, 'mainapp/generic.html')

def elements(request):
    return render(request, 'mainapp/elements.html')