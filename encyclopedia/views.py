from django.shortcuts import redirect, render
from . import util
from markdown2 import Markdown
from django.urls import reverse
from django.http.response import HttpResponseRedirect
from django import forms
import random

class NewEntry(forms.Form):
    entrytitle = forms.CharField(label="Title", max_length=30, widget=forms.TextInput(attrs={'class': 'form-control w-25'}))
    entrycontent = forms.CharField(label="Content", widget=forms.Textarea(attrs={'class': 'form-control w-50', 'rows': 15}))
    editentry = forms.BooleanField(initial=False, widget=forms.HiddenInput(), required=False)


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, entry):
    entryGet = util.get_entry(entry)
    markdowner = Markdown()
    if entryGet == None:
        return render(request, "encyclopedia/entrynotfound.html", {
            "entryname": entry
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "entryname": entry,
            "entry": markdowner.convert(entryGet)
        })


def entrysearch(request):
    get = request.GET.get("q").strip()
    search = get.lower()
    redirect = HttpResponseRedirect(reverse("entry", kwargs={"entry": search}))
    if util.get_entry(search) != None:
        return redirect
    else:
        suggestions = []
        for entry in util.list_entries():
            if search in entry.lower().strip():
                suggestions.append(entry)
        if len(suggestions) > 0:
            return render(request, "encyclopedia/entrysearch.html", {
                "suggestions": suggestions,
                "get": get,
                "results": len(suggestions)
            })
        else:
            return redirect


def entrynew(request):
    lower = []
    if request.method == "POST":
        form = NewEntry(request.POST)
        if form.is_valid():
            title = form.cleaned_data["entrytitle"]
            content = form.cleaned_data["entrycontent"]
            for entries in util.list_entries():
                lower.append(entries.lower())
            if title.lower() not in lower or form.cleaned_data["editentry"] is True:
                    util.save_entry(title, content)
                    return HttpResponseRedirect(reverse("entry", kwargs={"entry": title}))
            else:
                return render(request, "encyclopedia/entrynew.html", {
                    "form": NewEntry,
                    "exist": True   
                })
    return render(request, "encyclopedia/entrynew.html", {
        "form": NewEntry
    })


def entryedit(request, entry):
    entryPage = util.get_entry(entry)
    if entryPage is None:
        return render(request, "encyclopedia/entrynotfound.html", {
            "entrytitle": entry
        })
    else:
        entryform = NewEntry()
        entryform.fields["entrycontent"].initial = entryPage
        entryform.fields["entrytitle"].initial = entry
        entryform.fields["entrytitle"].widget = forms.HiddenInput()
        entryform.fields["editentry"].initial = True
        return render(request, "encyclopedia/entrynew.html", {
            "form": entryform,
            "edit": entryform.fields["editentry"].initial,
            "title": entryform.fields["entrytitle"].initial
        })

def entryrandom(request):
    entrieslist = util.list_entries()
    entryrandom = random.choice(entrieslist)
    return HttpResponseRedirect(reverse("entry", kwargs={"entry": entryrandom}))