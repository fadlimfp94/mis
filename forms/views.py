from django.shortcuts import render

from django.http import HttpResponse

# Create your views here.

def index(request):
    return HttpResponse("Hello, world. You're at the form index.")
	
def create_form(request):    
    return render(request, 'forms/form.html', {})