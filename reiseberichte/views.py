from django.http import Http404, HttpResponse
from django.shortcuts import render
from .models import Reise, Termin, Tag
from django.views.generic import CreateView
from django.template import loader
from datetime import date, timedelta, timezone, datetime


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


def reiseseite(request, reise_kurzel):
    try:
        reise = Reise.objects.get(reisekurzel=reise_kurzel)
    except Reise.DoesNotExist:
        raise Http404("Diese Reise existiert nicht")
    return HttpResponse("Reise " + reise_kurzel)


def terminseite(request, datum, reise_kurzel):
    try:
        reise = Reise.objects.get(reisekurzel=reise_kurzel)
    except Reise.DoesNotExist:
        raise Http404("Diese Reise existiert nicht")
    try:
        reisedatum = datetime.strptime(datum, "%y%m%d")
        abgleich = Termin.objects.get(reisebeginn=reisedatum)
    except Termin.DoesNotExist:
        raise Http404("Dieser Termin existiert nicht!")
    termin_daten = abgleich
    tage = Tag.objects.filter(reisedatum=abgleich)
    context = {
        'termin': termin_daten,
        'tage': tage,
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

class add_day(CreateView):
    model = Tag
    fields = ['reisetag', 'foto', 'beschreibung']
    reise_id = 1

"""
    class TagForm(CreateView, request, reise_kurzel):
    kurzel = reise_kurzel
    model = Tag
    fields = ['foto', 'beschreibung', 'reise', 'reisedatum', 'reiseleiter']
    data = {'reise': reise_kurzel}
    f = TagForm(data)
"""
