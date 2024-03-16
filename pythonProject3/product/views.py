from django.shortcuts import render
from django.shortcuts import HttpResponse


# Create your views here.
def index(request):
    return render(request,'index.html',{'Name':'Rumman'})


def index1(request):
    return HttpResponse("Hello this is new")

def add(request):
    val1=int(request.POST['num1'])
    val2=int(request.POST['num2'])
    sum=val1+val2

    return render(request,'basic.html',{'result':sum})
  # return render(request,'index.html',{'Name':'Rumman'})

