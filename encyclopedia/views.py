from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from . import util


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

def rp(request):
    pass