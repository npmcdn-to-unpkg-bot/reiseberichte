from .forms import TagForm
from .models import Reise, Termin, Tag
from datetime import date, timedelta, timezone, datetime
from django.contrib import messages
from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template import loader
from django.views.generic import CreateView



# Alle Reisen, die unterwegs sind, anzeigen. Wenn es Fotos gibt, dann das neueste, sonst Standardbild der Reise
def uebersicht(request):
    tag = Tag.objects.all()
    termin = Termin.objects.all().prefetch_related('reisename__tag_set')
    tage = Tag.objects.select_related('reisedatum').all().order_by('reisedatum')
    today = date.today()
    # Endtermin auslesen!!!!
    unterwegs=Termin.objects.filter(reiseende__gte=today).filter(reisebeginn__lte=today)
    context = {
        'termin': termin,
        'tag': tag,
        'tage': tage,
        'unterwegs': unterwegs,
                }
    return render(request, 'reiseberichte/uebersicht.html', context)

def tagkarte(request):
    return render(request, 'reiseberichte/tagkarte.html')

def reiseseite(request, reise_slug):
    reise = get_object_or_404(Reise, slug=reise_slug)
    return HttpResponse("Reise " + str(reise))


def terminseite(request, reise_slug, termin_slug):
    try:
        reise = Reise.objects.get(slug=reise_slug)
    except Reise.DoesNotExist:
        raise Http404("Diese Reise existiert nicht")
    termin = get_object_or_404(Termin, slug=termin_slug)
    tage = termin.termine.all().order_by('reisetag', 'created')
    context = {
        'tage': tage,
        'termin': termin,
    }
    return render(request, 'reiseberichte/termine.html', context)

def tagseite(request, datum, reise_kurzel, tag):
    try:
        tag_auswahl = Tag.objects.get(reisetag=tag)
    except Tag.DoesNotExist:
        raise Http404("Dieser Tag wurde nicht gefunden!")
    context = {
        'tag': tag_auswahl,
    }
    return render(request, 'reiseberichte/tagesansicht.html', context)

def add_day(request, reise_slug, termin_slug):
    termin = Termin.objects.get(slug=termin_slug)
    tag_nr = termin.termine.count() + 1
    data = {'reisetag': tag_nr}
    form = TagForm(initial=data)
    context = {
        'termin': termin,
        'form': form
    }
    if request.method == "POST":
        form = TagForm(request.POST, request.FILES)
        if form.is_valid():
            tag = form.save(commit=False)
            reise = Reise.objects.get(slug=reise_slug)
            tag.reise = reise
            tag.reisedatum = termin
            # tag.koordinaten = form.koordinaten
            # tag.koordinateneckig = form.koordinateneckig
            tag.save()
            messages.success(request, "Tag hinzugefügt!")
            return redirect('terminseite', reise_slug=reise_slug, termin_slug=termin_slug)
    else:
        form = TagForm(initial=data)
    return render(request, 'reiseberichte/tag_form.html', {'form': form, 'termin':termin})

"""
    class TagForm(CreateView, request, reise_kurzel):
    kurzel = reise_kurzel
    model = Tag
    fields = ['foto', 'beschreibung', 'reise', 'reisedatum', 'reiseleiter']
    data = {'reise': reise_kurzel}
    f = TagForm(data)
"""
