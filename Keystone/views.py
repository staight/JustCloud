from django.shortcuts import render, HttpResponse, redirect
from SqlMaster.models import *
import  hashlib
# Create your views here.
# pwd = Users.objects.filter(username=15002837903).values("password")[0]
# hashlib.sha1(pwd[0].encode(encoding='utf8')).hexdigest()== pwd[0]

def admin(request):
    return HttpResponse("敬请期待")

def login(request):
    if request.method == "POST":
        print(request)
        return 'success'

def register(request):
    if request.method == "GET":
        pass
    if request.method == "POST":
        pass
    return render(request,"register.html",locals())