from django.db import models
from uuslug import uuslug
from datetime import timedelta, datetime
import PIL.ExifTags
from PIL.ExifTags import TAGS
import PIL.Image
from geopy.geocoders import GeoNames




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
    slug = models.CharField(max_length=200, editable=False)

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = uuslug(self.reisename, instance=self)
        super(Reise, self).save(*args, **kwargs)

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


class Termin(TimeStampedModel):
    reisename = models.ForeignKey(Reise, related_name='reise')
    reisebeginn = models.DateField()
    reiseleiter = models.ForeignKey(Reiseleiter, on_delete=models.CASCADE)
    objects=models.Manager()
    reiseende = models.DateField(editable=False)
    favorite = models.BooleanField(editable=False, default=False)
    slug = models.TextField(max_length=100, editable=False)

    # Berechnung des Reiseendes und Slug aus Reisebeginn z.B. 160520
    def save(self, *args, **kwargs):
        self.reiseende = self.reisebeginn + timedelta(days=self.reisename.dauer)
        datum = datetime.strftime(self.reisebeginn, "%y%m%d")
        self.slug = uuslug(datum, instance=self)
        super(Termin, self).save(*args, **kwargs)

    # Methode, um den neuesten zugeordneten Tag zum Termin zu holen, ausgehend vom Foto
    def get_latest_foto(self):
        return Tag.objects.filter(reisedatum=self).last()

    # Plural Anzeige im Admin
    class Meta:
        verbose_name_plural = "Termine"

    def __str__(self):
        return self.reisename.reisekurzel+" - "+ self.slug

    def __unicode__(self):
        return self.reisebeginn


class Tag(TimeStampedModel):
    reisetag = models.IntegerField()
    foto = models.ImageField()
    beschreibung = models.TextField(max_length=1000)
    ort = models.CharField(max_length=50)
    reise = models.ForeignKey(Reise, models.CASCADE)
    reisedatum = models.ForeignKey(Termin, models.CASCADE, related_name='termine')
    koordinaten = models.CharField(max_length=100, editable=False, )
    koordinateneckig = models.CharField(max_length=100, editable=False, )


    def __str__(self):
        datum = str(self.reisedatum)
        tag = str(self.reisetag)
        kurzel = self.reise.reisekurzel
        return kurzel + ' Tag ' + tag

    def save(self, *args, **kwargs):
        # Nominatim ausgebaut
        geolocator = GeoNames(username='yunusabd')
        location = geolocator.geocode(self.ort)
        self.koordinaten = location.latitude, location.longitude
        self.koordinateneckig = [location.latitude, location.longitude]
        super(Tag, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Tage"

    # GPS Koordinaten aus EXIF auslesen --> gibt KeyError
    # def get_exif_data(self):
    #     """Returns a dictionary from the exif data of an PIL Image item. Also converts the GPS Tags"""
    #     img=PIL.Image.open(self.foto)
    #     exif_data = {}
    #     info = img._getexif()
    #
    #     ret = {}
    #     for tag, value in info.items():
    #         decoded = TAGS.get(tag, tag)
    #         ret[decoded] = value
    #
    #         nsec = ret['GPSInfo'][2][2][0] / float(ret['GPSInfo'][2][2][1])
    #         nmin = ret['GPSInfo'][2][1][0] / float(ret['GPSInfo'][2][1][1])
    #         ndeg = ret['GPSInfo'][2][0][0] / float(ret['GPSInfo'][2][0][1])
    #         wsec = ret['GPSInfo'][4][2][0] / float(ret['GPSInfo'][4][2][1])
    #         wmin = ret['GPSInfo'][4][1][0] / float(ret['GPSInfo'][4][1][1])
    #         wdeg = ret['GPSInfo'][4][0][0] / float(ret['GPSInfo'][4][0][1])
    #
    #         if ret['GPSInfo'][1] == 'N':
    #             nmult = 1
    #         else:
    #             nmult = -1
    #
    #         if ret['GPSInfo'][3] == 'E':
    #             wmult = 1
    #         else:
    #             wmult = -1
    #
    #         lat = nmult * (ndeg + (nmin + nsec / 60.0) / 60.0)
    #         lng = wmult * (wdeg + (wmin + wsec / 60.0) / 60.0)
    #
    #         return [lat, lng]


