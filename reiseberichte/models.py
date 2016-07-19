from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.urlresolvers import reverse
from datetime import timedelta, datetime, date


class TimeStampedModel(models.Model):
    # Abstract base class model to add 'created' and 'modified' fields to all models.
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateField(auto_now_add=True)

    class Meta:
        abstract = True


class Reise(TimeStampedModel):
    reisekurzel = models.CharField(max_length=20, verbose_name='Kürzel')
    reisename = models.CharField(max_length=100)
    beschreibung = models.TextField(max_length=1000)
    link = models.CharField(max_length=500)
    dauer = models.IntegerField()
    reiseheader = models.ImageField(verbose_name="Titelbild der Reise", default="media/China_mit_Yangtze.jpg")

    def __str__(self):
        return self.reisename

    class Meta:
        verbose_name_plural = "Reisen"


class Reiseleiter(TimeStampedModel):
    name = models.CharField(max_length=30)
    aktiv = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Reiseleiter"

'''class TerminManager(models.Manager):
    use_for_related_fields=True
    def aktiv(self):
        qs = self.get_queryset()
        reisebeginn = qs.reisebeginn
        dauer = 23
        ende = reisebeginn+timedelta(days=dauer)
        return super(TerminManager, self).qs.get(id=5)'''

#class TerminManager(models.Manager):
#    def unterwegs(self):

class Termin(TimeStampedModel):
    reisename = models.ForeignKey(Reise, related_name='reise')
    reisebeginn = models.DateField()
    reiseleiter = models.ForeignKey(Reiseleiter, on_delete=models.CASCADE)
    objects=models.Manager()
    reiseende = models.DateField(editable=False)
    favorite = models.BooleanField(editable=False, default=False)

    # Berechnung des Reiseendes
    def save(self, *args, **kwargs):
        self.reiseende = self.reisebeginn + timedelta(days=self.reisename.dauer)
        super(Termin, self).save(*args, **kwargs)

    # Methode, um den neuesten zugeordneten Tag zum Termin zu holen, ausgehend vom Foto
    def get_latest_foto(self):
        return Tag.objects.filter(reisedatum=self).latest("foto")

    # PLural Anzeige im Admin
    class Meta:
        verbose_name_plural = "Termine"

    def __str__(self):
        return self.reisename.reisekurzel+" - "+str(self.reisebeginn)


class Tag(TimeStampedModel):
    reisetag = models.IntegerField()
    foto = models.ImageField()
    beschreibung = models.TextField(max_length=1000)
    reise = models.ForeignKey(Reise, models.CASCADE)
    reisedatum = models.ForeignKey(Termin, models.CASCADE, related_name='termine')

    def __str__(self):
        datum = str(self.reisedatum)
        tag = str(self.reisetag)
        kurzel = self.reise.reisekurzel
        return kurzel + datum + ' Tag ' + tag

    class Meta:
        verbose_name_plural = "Tage"






