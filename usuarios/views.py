from django.shortcuts import render, HttpResponse

# Create your views here.
def cadastro(request):
    if request.method == "GET":
        return HttpResponse('Hello World')
        return render(request, 'cadastro.html')