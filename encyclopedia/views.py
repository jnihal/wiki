from django.shortcuts import render
from django import forms
from django.urls  import reverse
from django.http import HttpResponseRedirect, HttpResponse
import random

from . import util


class SearchForm(forms.Form):
    q = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={"class": "search", "placeholder": "Search Encyclopedia"}))


class NewPageForm(forms.Form):
    title = forms.CharField(
        label="",
        widget=forms.Textarea(attrs={"id": "titlearea", "placeholder": "Enter the title for the page here"})
    )
    content = forms.CharField(
        label="",
        widget=forms.Textarea(attrs={"class": "textarea", "placeholder": "Enter the Markdown content for the page here."})
    )

    def clean_title(self):
        title = self.cleaned_data.get("title")

        if util.titleExists(title):
            raise forms.ValidationError("Title already exists")
        return title


class EditForm(forms.Form):
    content = forms.CharField(
        label="",
        widget=forms.Textarea(attrs={"class": "textarea"})
    )


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "searchForm": SearchForm()
    })


def displayContent(request, title):
    content = util.get_entry(title)
    
    if content != None:
        return render(request, "encyclopedia/contentPage.html", {
            "title": util.preserveCase(title),
            "content": util.markdownToHTML(util.get_entry(title)),
            "searchForm": SearchForm()
        })
    else:
        return render(request, "encyclopedia/errorPage.html", {
            "searchForm": SearchForm()
        })


def search(request):
    entries = util.list_entries()

    if request.method == "GET":
        form = SearchForm(request.GET)

        if form.is_valid():
            q = form.cleaned_data["q"]

            if q.lower() in (entry.lower() for entry in entries):
                return HttpResponseRedirect(reverse("title", args=[q]))

            for entry in entries.copy():
                if q.lower() in entry.lower():
                    continue
                entries.remove(entry)

            return render(request, "encyclopedia/searchPage.html", {
                "entries": entries,
                "searchForm": form
            })

        else:
            return render(request, "encyclopedia/index.html", {
                "entries": util.list_entries(),
                "searchForm": form
            })


def new(request):
    entries = util.list_entries()

    if request.method == "POST":
        form = NewPageForm(request.POST)

        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]

            util.save_entry(title, content)

            return HttpResponseRedirect(reverse("title", args=[title]))

        else:
            return render(request, "encyclopedia/newEntry.html", {
                "searchForm": SearchForm(),
                "newPageForm": form
            })

    return render(request, "encyclopedia/newEntry.html", {
        "searchForm": SearchForm(),
        "newPageForm": NewPageForm()
    })


def edit(request, title):
    if request.method == "GET":
        content = util.get_entry(title)
        form = EditForm(initial={"content": content})
        return render(request, "encyclopedia/editPage.html", {
            "title": title,
            "searchForm": SearchForm(),
            "editForm": form
        })
    
    else:
        form = EditForm(request.POST)

        if form.is_valid():
            content = form.cleaned_data["content"]

            util.save_entry(title, content)

            return HttpResponseRedirect(reverse("title", args=[title]))


def randomPage(request):
    entries = util.list_entries()
    title = random.choice(entries)
    return HttpResponseRedirect(reverse("title", args=[title]))