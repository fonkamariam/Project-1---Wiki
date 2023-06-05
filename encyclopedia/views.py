from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from . import util
import random


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def cnp(request):
    if request.method =='POST':
        title= request.POST["filename"]
        body=request.POST["body"]
        for name in util.list_entries():
            if name==title:
                return render(request,"encyclopedia/cnp.html",{"body":body,"message":f"Username '{title}' Taken...Try Again"})
        util.save_entry(title,body)
        return HttpResponseRedirect(reverse("index"))
    return render(request, "encyclopedia/cnp.html",{"names":util.list_entries})
def get(request,x):
    return render(request,f"encyclopedia/{x}.html")
def rp(request):
    listt=[]
    for x in util.list_entries():
        listt.append(x)
    a=random.choice(listt)
    return HttpResponseRedirect(reverse("get",kwargs={"x":a}))
def edit(request,y):
    if request.method =='POST':
        hidden=request.POST["old_title"]
        title= request.POST["filename"]
        body=request.POST["body"]
        util.delete_entry(hidden)
        util.save_entry(title,body)
        return HttpResponseRedirect(reverse("index"))
    a=util.get_entry(y)
    return render(request, "encyclopedia/editpage.html",{"fonka":a,"text":a,"title":y})
    