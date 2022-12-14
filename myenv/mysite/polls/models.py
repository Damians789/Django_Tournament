from django.core.exceptions import ValidationError

from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from django.db import models
import datetime
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.db.models import Max, Sum, UniqueConstraint
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField

from django.contrib.auth.models import User

# Create your models here.

from mysite import settings


class Wojewodztwo(models.Model):
    woj_nazwa = models.CharField(max_length=20, blank=False, unique=True)

    def __str__(self):
        return self.woj_nazwa


class Acode(models.Model):
    ZIP = models.CharField(max_length=6)
    Miasto = models.CharField(max_length=30)
    Woj = models.ForeignKey(Wojewodztwo, on_delete=models.CASCADE)
    Adres = models.ForeignKey('Adres', on_delete=models.SET_NULL, blank=True, null=True)

    # def __str__(self):
    #     return str(self.id)

    def __str__(self):
        return self.razem()

    def razem(self):
        return "{} ({}) {}".format(self.Miasto, self.ZIP, self.Woj)


class Adres(models.Model):
    Ulica = models.CharField(max_length=40)
    NrDomu = models.IntegerField(default=0)
    NrLokalu = models.IntegerField(blank=True, null=True)
    Acode = models.ForeignKey(Acode, related_name="has_titles", on_delete=models.CASCADE)

    def __str__(self):
        return self.razem()

    def razem(self):
        return "{}, ul. {} {}/{}, {}, {}".format(self.Acode.Miasto, self.Ulica, self.NrDomu, self.NrLokalu,
                                        self.Acode.ZIP, self.Acode.Woj)

    @property
    def category_name(self):
        return self.Acode.Miasto


class Stadion(models.Model):
    stadion_nazwa = models.CharField(max_length=100, blank=False, unique=True, verbose_name='Nazwa stadionu')
    pojemnosc_trybun = models.IntegerField(default=0, null=True, blank=True, verbose_name='Pojemność trybun')
    niepelnosprawni = models.BooleanField(default=False, verbose_name='Niepełnosprawni')
    stadion_adres = models.OneToOneField(Adres, on_delete=models.CASCADE, verbose_name='Adres stadionu')
    stadion_zdjecie = models.ImageField(upload_to="polls/images/", null=True, blank=True, verbose_name='Zdjęcie stadionu')
    naw_av = models.DecimalField(default=0, max_digits=3, decimal_places=2)
    sza_av = models.DecimalField(default=0, max_digits=3, decimal_places=2)
    org_av = models.DecimalField(default=0, max_digits=3, decimal_places=2)

    def __str__(self):
        return self.stadion_nazwa


def return_date_time():
    now = timezone.now()
    return now + datetime.timedelta(days=7)


class Zawody(models.Model):
    zawody_nazwa = models.CharField(max_length=200, verbose_name='Nazwa')
    zawody_data = models.DateTimeField(default=return_date_time, verbose_name='Kiedy', help_text='<em>DD.MM.YYYY HH:MM</em>')
    # zawody_data = models.DateTimeField(default=timezone.now, verbose_name='Kiedy')
    aff_url = models.SlugField(blank=True, null=True, help_text='wyrazy-oddzielone-myslnikami')
    zawody_pub = models.DateTimeField(auto_now_add=True)
    stadion = models.ForeignKey(Stadion, on_delete=models.CASCADE)

    @property
    def minely(self):
        return datetime.datetime.now() > self.zawody_data

    def __str__(self):
        return self.zawody_nazwa


class Team(models.Model):
    team_nazwa = models.CharField(max_length=50, blank=False, null=False, unique=True, verbose_name='Nazwa drużyny')

    def __str__(self):
        return self.team_nazwa


class Szatnia(models.Model):
    zawody = models.ForeignKey(Zawody, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    pokoj = models.CharField(max_length=5, blank=False, null=True)


class Osoba(models.Model):
    Trener = 'trener'
    Zawodnik = 'zawodnik'
    STATUS = (
        (Zawodnik, 'Konto zawodnika'),
        (Trener, 'Konto trenera'),
    )
    imie = models.CharField(max_length=50, blank=False, null=False, verbose_name='Imię')
    nazwisko = models.CharField(max_length=50, blank=False, null=False, verbose_name='Nazwisko')
    data_urodzenia = models.DateField(default=timezone.now, blank=False, null=False, verbose_name='Data Urodzenia', help_text='dd.mm.rrrr')
    # phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Numer telefonu musi być w formacie: '+999999999'. Dozwolone 15. cyfr.")
    telefon = PhoneNumberField()
    email = models.EmailField(blank=True, null=True, verbose_name='Email')
    zdjecie = models.ImageField(upload_to="polls/images/", null=True, blank=True, verbose_name='Zdjęcie')
    adres = models.ForeignKey(Adres, on_delete=models.SET_NULL, blank=False, null=True)
    team = models.ManyToManyField(Team)
    status = models.CharField(max_length=20, choices=STATUS, default=Zawodnik)

    def __str__(self):
        return self.razem()

    def razem(self):
        return "{} {} ({})".format(self.imie, self.nazwisko, self.status)


class Zawodnik(models.Model):
    zawodnik_imie = models.CharField(max_length=50, blank=False, null=False)
    zawodnik_nazwisko = models.CharField(max_length=50, blank=False, null=False)
    zawodnik_wiek = models.IntegerField(default=0, blank=False, null=False)
    zawodnik_telefon = models.IntegerField(default=0, blank=False, null=False)
    zawodnik_email = models.EmailField(blank=True, null=True)
    zawodnik_adres = models.ForeignKey(Adres, on_delete=models.SET_NULL, blank=False, null=True)
    zawodnik_team = models.ManyToManyField(Team)

    def __str__(self):
        return self.razem()

    def razem(self):
        return "{} {}".format(self.zawodnik_imie, self.zawodnik_nazwisko)


class Trener(models.Model):
    trener_imie = models.CharField(max_length=50, blank=False, null=False)
    trener_nazwisko = models.CharField(max_length=50, blank=False, null=False)
    trener_wiek = models.IntegerField(default=0, blank=False, null=False)
    trener_telefon = models.IntegerField(default=0, blank=False, null=False)
    trener_email = models.EmailField(blank=True, null=True)
    trener_adres = models.ForeignKey(Adres, on_delete=models.SET_NULL, blank=False, null=True)
    trener_team = models.ManyToManyField(Team)

    def __str__(self):
        return self.razem()

    def razem(self):
        return "{} {}".format(self.trener_imie, self.trener_nazwisko)


class Dyscyplina(models.Model):
    dyscyplina_nazwa = models.CharField(max_length=100, blank=False, null=False)
    zaw_1 = models.ForeignKey(Osoba, on_delete=models.SET_NULL, null=True, related_name='uno')
    top_1 = models.DecimalField(default=0, max_digits=6, decimal_places=2, null=True, blank=True)
    zaw_2 = models.ForeignKey(Osoba, on_delete=models.SET_NULL, null=True, related_name='dos')
    top_2 = models.DecimalField(default=0, max_digits=6, decimal_places=2, null=True, blank=True)
    zaw_3 = models.ForeignKey(Osoba, on_delete=models.SET_NULL, null=True, related_name='tres')
    top_3 = models.DecimalField(default=0, max_digits=6, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.dyscyplina_nazwa


class Lista_Zawodnikow(models.Model):
    Osoba = models.ForeignKey(Osoba, on_delete=models.CASCADE, null=True)
    Zawody = models.ForeignKey(Zawody, on_delete=models.CASCADE, null=True)
    Dyscyplina = models.ForeignKey(Dyscyplina, on_delete=models.CASCADE, null=True)
    Czas_Odleglosc = models.DecimalField(default=0, max_digits=6, decimal_places=2, null=True, blank=True)

    def calc(self):
        dysc = self.Dyscyplina
        zaw = self.Osoba
        l_dysc = Lista_Zawodnikow.objects.filter(Dyscyplina=dysc)
        ord_lista = l_dysc.order_by('-Czas_Odleglosc')
        l_zaw = Lista_Zawodnikow.objects.filter(Osoba=zaw)
        ord_zaw = l_zaw.order_by('-Czas_Odleglosc')
        top = ord_lista.values_list('Czas_Odleglosc', flat=True)
        topz = ord_zaw.values_list('Osoba', flat=True)
        if top[0] >= Dyscyplina.top1:
            Dyscyplina.top1 = top[0]
            Dyscyplina.zaw1 = topz[0]
        elif top >= Dyscyplina.top2:
            Dyscyplina.top2 = top[0]
            Dyscyplina.zaw2 = topz[0]
        elif top >= Dyscyplina.top3:
            Dyscyplina.top3 = top[0]
            Dyscyplina.zaw3 = topz[0]
        Dyscyplina.save(self)


# class myuser(AbstractUser):
#     wiek = models.IntegerField(default=0, blank=False, null=False)
#     telefon = models.IntegerField(default=0, blank=False, null=False)
#     adres = models.ForeignKey(Adres, on_delete=models.SET_NULL, blank=False, null=True)
#     team = models.ManyToManyField(Team)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    osoba = models.OneToOneField(Osoba, on_delete=models.SET_NULL, null=True, blank=True, unique=True)
    zawody = models.ManyToManyField(Zawody, blank=True)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()


# class ProfileTrener(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     trener = models.ForeignKey(Trener, on_delete=models.CASCADE)
#
#     @receiver(post_save, sender=User)
#     def create_user_profile(sender, instance, created, **kwargs):
#         if created:
#             ProfileZawodnik.objects.create(user=instance)
#
#     @receiver(post_save, sender=User)
#     def save_user_profile(sender, instance, **kwargs):
#         instance.profile.save()


class Vote(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
    stadion = models.ForeignKey(Stadion, on_delete=models.CASCADE)
    nawierzchnia = models.IntegerField(default=0, null=True)
    szatnie = models.IntegerField(default=0, null=True)
    organizacja = models.IntegerField(default=0, null=True)

    def calculate_averages(self):
        stadion = self.stadion
        vote_qs = Vote.objects.filter(stadion=stadion)
        vote_count = vote_qs.count()
        nawierzchnia_total = vote_qs.aggregate(Sum('nawierzchnia'))
        szatnie_total = vote_qs.aggregate(Sum('szatnie'))
        organizacja_total = vote_qs.aggregate(Sum('organizacja'))
        stadion.naw_av = nawierzchnia_total['nawierzchnia__sum']/vote_count
        stadion.sza_av = szatnie_total['szatnie__sum']/vote_count
        stadion.org_av = organizacja_total['organizacja__sum']/vote_count
        stadion.save()

    # def validate_unique(self, *args, **kwargs):
    #     super(Vote, self).validate_unique(*args, **kwargs)
    #
    #     if self.__class__.objects. \
    #             filter(profile=self.profile, stadion=self.stadion). \
    #             exists():
    #         raise ValidationError(
    #             message='Vote with this (profile, stadion) already exists.',
    #             code='unique_together',
    #         )
