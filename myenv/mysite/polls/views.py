import json

from django.db.models import Count
from django.forms.models import model_to_dict

from django.db import transaction
from django.shortcuts import render
from django.views.generic import DetailView
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserCreationForm, UserForm, ProfileForm
from .forms import *
from .models import *

from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.core.mail import send_mail, BadHeaderError
from django.contrib import messages
from django.db.models.query_utils import Q
from django.contrib.auth import authenticate, login, logout, get_user_model


def homepage(request):
    # if request.method == "POST":
    #     id_stadion = request.POST.get("id")
    #     stadion = Stadion.objects.get(id=id_stadion)
    #     request.user.profile.films.add(movie)
    #     messages.success(request, f'{movie} added to wishlist.')
    #     return redirect('polls:homepage')
    stadion = Stadion.objects.all()
    zawody = Zawody.objects.all()[:3]
    new_posts = Zawody.objects.all().order_by('-zawody_pub')
    kiedy = Zawody.objects.all().order_by('-zawody_data')
    most_recent = new_posts.first()
    return render(request=request, template_name="base.html",
                  context={'zawody': zawody, 'most_recent': most_recent, "new_posts": new_posts, "kiedy": kiedy,
                           'stadion': stadion})


def article(request, strona):
    ok = Zawody.objects.get(aff_url=strona)
    return render(request=request, template_name='article.html', context={"ok": ok})


def userpage(request):
    if request.method == "POST":
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, 'Your profile was successfully updated!')
        elif profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Your wishlist was successfully updated!')
        else:
            messages.error(request, 'Unable to complete request')
        return redirect("polls:userpage")
    user_form = UserForm(instance=request.user)
    profile_form = ProfileForm(instance=request.user.profile)
    return render(request=request, template_name="user.html", context={"user": request.user, "user_form": user_form,
                                                                       "profile_form": profile_form})


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend', )
            messages.success(request, "Registration successful.")
            return redirect("polls:homepage")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = UserCreationForm
    return render(request=request, template_name="registration/signup.html", context={"form": form})


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}")
                return redirect("polls:homepage")
            else:
                messages.error(request, "Invalid username or password")
        else:
            messages.error(request, "Invalid username or password")
    form = AuthenticationForm()
    return render(request=request, template_name="registration/login.html", context={"form": form})


def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("polls:homepage")


def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "registration/password_reset_email.txt"
                    c = {
                        "email": user.email,
                        'domain': '127.0.0.1:8000',
                        'site_name': 'Stronka',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'admin@example.com', [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')

                    messages.success(request, 'A message with reset password instructions has been sent to your inbox.')
                    return redirect("polls:homepage")
            messages.error(request, 'An invalid email has been entered.')
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="registration/password_reset.html",
                  context={"password_reset_form": password_reset_form})


class crwoj(CreateView):
    model = Wojewodztwo
    fields = ('id', 'woj_nazwa')
    template_name = "dodaj.html"
    success_url = "/"


class upwoj(UpdateView):
    model = Wojewodztwo
    fields = ('id', 'woj_nazwa')
    template_name = 'dodaj.html'
    success_url = '/'


class dewoj(DeleteView):
    model = Wojewodztwo
    template_name = 'usun.html'
    success_url = '/'


def woj(request):
    if request.method == "POST":
        if "testo" in request.POST:
            uwoj = WojForm(request.POST)
            if uwoj.is_valid():
                title = uwoj.cleaned_data.get("woj_nazwa")
                uwoj.save()
                messages.success(request, f'{title} dodane.')
                return redirect('polls:woj')
            messages.error(request, 'Form jest niepoprawny.')
        if "atest" in request.POST:
            uacode = AcodeForm2(request.POST)
            if uacode.is_valid():
                title = uacode.cleaned_data.get("Miasto")
                uacode.save()
                messages.success(request, f'{title} dodane.')
                return redirect('polls:woj')
            messages.error(request, 'Form jest niepoprawny.')
        if "adtest" in request.POST:
            uadres = AdresForm2(request.POST)
            if uadres.is_valid():
                title = uadres.cleaned_data.get("Ulica")
                uadres.save()
                messages.success(request, f'{title} dodane.')
                return redirect('polls:woj')
            messages.error(request, 'Form jest niepoprawny.')

    woj = Wojewodztwo.objects.all()
    paginator = Paginator(woj, 16)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    uwoj = WojForm()

    acode = Acode.objects.all()
    apaginator = Paginator(acode, 16)
    apage_number = request.GET.get('page')
    apage_obj = apaginator.get_page(apage_number)
    uacode = AcodeForm2()

    adres = Adres.objects.all()
    adpaginator = Paginator(adres, 16)
    adpage_number = request.GET.get('page')
    adpage_obj = adpaginator.get_page(adpage_number)
    uadres = AdresForm2()

    return render(request=request, template_name="woj.html", context={"page_obj": page_obj, "uwoj": uwoj,
                                                                      "apage_obj": apage_obj, "uacode": uacode,
                                                                      "adpage_obj": adpage_obj, "uadres": uadres,
                                                                      })


# class cracode(CreateView):
#     model = Acode
#     template_name = "dodaj.html"
#     form_class = AcodeForm
#     success_url = None
#
#     def get_context_data(self, **kwargs):
#         data = super(cracode, self).get_context_data(**kwargs)
#         if self.request.POST:
#             data['titles'] = cos(self.request.POST)
#         else:
#             data['titles'] = cos()
#         return data
#
#     def form_valid(self, form):
#         context = self.get_context_data()
#         titles = context['titles']
#         with transaction.atomic():
#             # form.instance.created_by = self.request.user
#             self.object = form.save()
#             if titles.is_valid():
#                 titles.instance = self.object
#                 titles.save()
#         return super(cracode, self).form_valid(form)
#
#     def get_success_url(self):
#         return reverse_lazy('polls:woj', kwargs={'pk': self.object.pk})
#
#
# class upacode(UpdateView):
#     model = Acode
#     form_class = AcodeForm
#     template_name = 'dodaj.html'
#
#     def get_context_data(self, **kwargs):
#         data = super(upacode, self).get_context_data(**kwargs)
#         if self.request.POST:
#             data['titles'] = cos(self.request.POST, instance=self.object)
#         else:
#             data['titles'] = cos(instance=self.object)
#         return data
#
#     def form_valid(self, form):
#         context = self.get_context_data()
#         titles = context['titles']
#         with transaction.atomic():
#             # form.instance.created_by = self.request.user
#             self.object = form.save()
#             if titles.is_valid():
#                 titles.instance = self.object
#                 titles.save()
#         return super(upacode, self).form_valid(form)
#
#     def get_success_url(self):
#         return reverse_lazy('polls:woj', kwargs={'pk': self.object.pk})


class cracode(CreateView):
    model = Acode
    fields = ('ZIP', 'Miasto', 'Woj')
    template_name = "dodaj.html"
    success_url = "/woj/"


class upacode(UpdateView):
    model = Acode
    fields = ('ZIP', 'Miasto', 'Woj')
    template_name = 'dodaj.html'
    success_url = '/woj/'


class deacode(DeleteView):
    model = Acode
    template_name = 'usun.html'
    success_url = '/woj/'


# def acode(request):
#     if request.method == "POST":
#         if "atest" in request.POST:
#             uacode = AcodeForm(request.POST)
#             if uacode.is_valid():
#                 title = uacode.cleaned_data.get("Miasto")
#                 uacode.save()
#                 messages.success(request, f'{title} dodane.')
#                 return redirect('polls:acode')
#             messages.error(request, 'Form jest niepoprawny.')
#     acode = Acode.objects.all()
#     uacode = AcodeForm()
#     return render(request=request, template_name="woj.html", context={"acode": acode, "uacode": uacode})


class seeadres(DetailView):
    model = Adres
    template_name = 'adres.html'

    def get_context_data(self, **kwargs):
        context = super(seeadres, self).get_context_data(**kwargs)
        return context


# class cradres(CreateView):
#     model = Adres
#     template_name = "dodaj.html"
#     form_class = AdresForm3
#     success_url = '/woj/'
#
#     def get_context_data(self, **kwargs):
#         data = super(cradres, self).get_context_data(**kwargs)
#         if self.request.POST:
#             data['titles'] = cos2(self.request.POST)
#         else:
#             data['titles'] = cos2()
#         return data
#
#     def form_valid(self, form):
#         context = self.get_context_data()
#         titles = context['titles']
#         with transaction.atomic():
#             # form.instance.Acode = self.request.Acode
#             self.object = form.save()
#             if titles.is_valid():
#                 titles.instance = self.object
#                 titles.save()
#         return super(cradres, self).form_valid(form)
#
#     def get_success_url(self):
#         return reverse_lazy('polls:adres_det', kwargs={'pk': self.object.pk})


class cradres(CreateView):
    model = Adres
    fields = ('Ulica', 'NrDomu', 'NrLokalu', 'Acode')
    template_name = "dodaj.html"
    success_url = "/woj/"


# class upadres(UpdateView):
#     model = Adres
#     form_class = AdresForm3
#     template_name = 'dodaj.html'
#
#     def get_context_data(self, **kwargs):
#         data = super(upadres, self).get_context_data(**kwargs)
#         if self.request.POST:
#             data['titles'] = cos2(self.request.POST, instance=self.object)
#         else:
#             data['titles'] = cos2(instance=self.object)
#         return data
#
#     def form_valid(self, form):
#         context = self.get_context_data()
#         titles = context['titles']
#         with transaction.atomic():
#             # form.instance.Acode = self.request.Acode
#             self.object = form.save()
#             if titles.is_valid():
#                 titles.instance = self.object
#                 titles.save()
#         return super(upadres, self).form_valid(form)
#
#     def get_success_url(self):
#         return reverse_lazy('polls:adres_det', kwargs={'pk': self.object.pk})


class upadres(UpdateView):
    model = Adres
    fields = ('Ulica', 'NrDomu', 'NrLokalu', 'Acode')
    template_name = 'dodaj.html'
    success_url = '/woj/'


class deadres(DeleteView):
    model = Adres
    template_name = 'usun.html'
    success_url = '/woj/'


class crstadion(CreateView):
    model = Stadion
    fields = '__all__'
    template_name = "dodaj.html"
    success_url = "/stadion/"


class upstadion(UpdateView):
    model = Stadion
    fields = '__all__'
    template_name = 'dodaj.html'
    success_url = '/stadion/'


class destadion(DeleteView):
    model = Stadion
    template_name = 'usun.html'
    success_url = '/stadion/'


def stadion(request):
    if request.method == "POST":
        if "score_submit" in request.POST:
            vote_form = VoteForm(request.POST)
            if vote_form.is_valid():
                form = vote_form.save(commit=False)
                form.profile = request.user.profile
                stadion_id = request.POST.get("stadion")
                form.stadion = Stadion.objects.get(id=stadion_id)
                form.save()
                form.calculate_averages()
                messages.success(request, f'Ocena stadionu {form.stadion} dodana.')
                return redirect('polls:stadion')
            messages.error(request, 'Form jest niepoprawny.')
            return redirect('polls:stadion')
        if "testo" in request.POST:
            test = StadionForm(request.POST, request.FILES)
            if test.is_valid():
                title = test.cleaned_data.get("stadion_nazwa")
                test.save()
                messages.success(request, f'{title} stadion dodany.')
                return redirect('polls:stadion')
            return redirect('polls:stadion')
        # id_film = request.POST.get("id_film")
        # film = Film.objects.get(id_film=id_film)
        # request.user.profile.films.add(film)
        # messages.success(request, f'{film} added to wishlist.')
        # return redirect('polls:films')
    stadion = Stadion.objects.all()
    paginator = Paginator(stadion, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    vote_form = VoteForm()
    test = StadionForm()
    return render(request=request, template_name="stadion.html",
                  context={"stadion": stadion, "page_obj": page_obj, "vote_form": vote_form, "test": test})


def zawody(request):
    if request.method == "POST":
        if "testo" in request.POST:
            uzawody = ZawodyForm(request.POST)
            if uzawody.is_valid():
                title = uzawody.cleaned_data.get("zawody_nazwa")
                uzawody.save()
                messages.success(request, f'Zawody {title} dodane.')
                return redirect('polls:zawody')
            messages.error(request, 'Form jest niepoprawny.')

        id_zawody = request.POST.get("id_zawody")
        zawody = Zawody.objects.get(id=id_zawody)
        request.user.profile.zawody.add(zawody)
        messages.success(request, f'Zawody dodane do profilu {zawody}')
        return redirect('polls:zawody')
    zawody = Zawody.objects.all()
    paginator = Paginator(zawody, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    uzawody = ZawodyForm()

    return render(request=request, template_name="zawody.html", context={"page_obj": page_obj, "uzawody": uzawody,
                                                                         })


class crzawody(CreateView):
    model = Zawody
    fields = 'zawody_nazwa', 'zawody_data', 'aff_url', 'stadion'
    template_name = "dodaj.html"
    success_url = "/zawody/"


class upzawody(UpdateView):
    model = Zawody
    fields = 'zawody_nazwa', 'zawody_data', 'aff_url', 'stadion'
    template_name = 'dodaj.html'
    success_url = '/zawody/'


class dezawody(DeleteView):
    model = Zawody
    template_name = 'usun.html'
    success_url = '/zawody/'


def team(request):
    if request.method == "POST":
        if "testo" in request.POST:
            uteam = TeamForm(request.POST)
            if uteam.is_valid():
                title = uteam.cleaned_data.get("team_nazwa")
                uteam.save()
                messages.success(request, f'Drużyna {title} dodane.')
                return redirect('polls:team')
            messages.error(request, 'Form jest niepoprawny.')

    team = Team.objects.all()
    paginator = Paginator(team, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    uteam = TeamForm()

    return render(request=request, template_name="team.html", context={"page_obj": page_obj, "uteam": uteam,
                                                                       })


class crteam(CreateView):
    model = Team
    fields = 'team_nazwa',
    template_name = "dodaj.html"
    success_url = "/team/"


class upteam(UpdateView):
    model = Team
    fields = 'team_nazwa',
    template_name = 'dodaj.html'
    success_url = '/team/'


class deteam(DeleteView):
    model = Team
    template_name = 'usun.html'
    success_url = '/team/'


def osoba(request):
    if request.method == "POST":
        if "testo" in request.POST:
            uosoba = OsobaForm(request.POST, request.FILES or None)
            if uosoba.is_valid():
                imie = uosoba.cleaned_data.get("imie")
                nazwisko = uosoba.cleaned_data.get("nazwisko")
                nazwa = imie + nazwisko
                uosoba.save()
                messages.success(request, f'Osoba {nazwa} dodana.')
                # return HttpResponseRedirect('')
                return redirect('polls:osoba')
            messages.error(request, 'Form osoba jest niepoprawny.')
        if "testo1" in request.POST:
            uacode = AcodeForm2(request.POST)
            if uacode.is_valid():
                title = uacode.cleaned_data.get("Miasto")
                uacode.save()
                messages.success(request, f'Adres 1 {title} dodany.')
                return redirect('polls:osoba')
            messages.error(request, 'Form acode jest niepoprawny.')
        if "testo2" in request.POST:
            uadres = AdresForm2(request.POST)
            if uadres.is_valid():
                title = uadres.cleaned_data.get("Ulica")
                uadres.save()
                messages.success(request, f'Adres 2 {title} dodany.')
                return redirect('polls:osoba')
            messages.error(request, 'Form adres jest niepoprawny.')

    osoba = Osoba.objects.all()
    paginator = Paginator(osoba, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    uosoba = OsobaForm()
    uacode = AcodeForm2()
    uadres = AdresForm2()

    return render(request=request, template_name="osoba.html", context={"page_obj": page_obj, "uosoba": uosoba,
                                                                        "uacode": uacode, "uadres": uadres})


class crosoba(CreateView):
    model = Osoba
    fields = 'imie', 'nazwisko', 'data_urodzenia', 'telefon', 'email', 'zdjecie', 'adres', 'team', 'status'
    template_name = "dodaj.html"
    success_url = "/osoba/"


class uposoba(UpdateView):
    model = Osoba
    fields = 'imie', 'nazwisko', 'data_urodzenia', 'telefon', 'email', 'zdjecie', 'adres', 'team', 'status'
    template_name = 'dodaj.html'
    success_url = '/osoba/'


class deosoba(DeleteView):
    model = Osoba
    template_name = 'usun.html'
    success_url = '/osoba/'


def szatnie(request):
    if request.method == "POST":
        if "testo" in request.POST:
            uszatnia = SzatniaForm(request.POST)
            if uszatnia.is_valid():
                title = uszatnia.cleaned_data.get("pokoj")
                uszatnia.save()
                messages.success(request, f'Szatnia {title} została przypisana.')
                return redirect('polls:szatnia')
            messages.error(request, 'Form jest niepoprawny.')

    szatnia = Szatnia.objects.all()
    paginator = Paginator(szatnia, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    uszatnia = SzatniaForm()

    return render(request=request, template_name="szatnia.html", context={"page_obj": page_obj, "uszatnia": uszatnia,
                                                                          })


class crszatnie(CreateView):
    model = Szatnia
    fields = 'zawody', 'team', 'pokoj'
    template_name = "dodaj.html"
    success_url = "/szatnia/"


class upszatnie(UpdateView):
    model = Szatnia
    fields = 'zawody', 'team', 'pokoj'
    template_name = 'dodaj.html'
    success_url = '/szatnia/'


class deszatnie(DeleteView):
    model = Szatnia
    template_name = 'usun.html'
    success_url = '/szatnia/'


def dyscyplina(request):
    if request.method == "POST":
        if "testo" in request.POST:
            udysc = DyscForm(request.POST)
            if udysc.is_valid():
                title = udysc.cleaned_data.get("dyscyplina_nazwa")
                udysc.save()
                messages.success(request, f'Dyscyplina {title} dodana.')
                return redirect('polls:dyscyplina')
            messages.error(request, 'Form jest niepoprawny.')

    dysc = Dyscyplina.objects.all()
    paginator = Paginator(dysc, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    udysc = DyscForm()
    d = dysc.values_list('zaw_1', flat=True)
    o1 = Osoba.objects.get(id=d.first())
    # o2 = Osoba.objects.get(id=dysc.dos)
    # o3 = Osoba.objects.get(id=dysc.tres)

    return render(request=request, template_name="dyscyplina.html", context={"dysc": dysc, "page_obj": page_obj, "udysc": udysc,
                                                                             "o1": o1,})


class crdyscyplina(CreateView):
    model = Dyscyplina
    fields = 'dyscyplina_nazwa'
    template_name = "dodaj.html"
    success_url = "/dyscyplina/"


class updyscyplina(UpdateView):
    model = Dyscyplina
    fields = 'dyscyplina_nazwa'
    template_name = 'dodaj.html'
    success_url = '/dyscyplina/'


class dedyscyplina(DeleteView):
    model = Dyscyplina
    template_name = 'usun.html'
    success_url = '/dyscyplina/'


def lista_zawodnikow(request):
    if request.method == "POST":
        if "testo" in request.POST:
            ulz = LZForm(request.POST)
            if ulz.is_valid():
                form = ulz.save(commit=False)
                form.save()
                # form.calc()
                messages.success(request, f'Lista {object} dodana.')
                return redirect('polls:lz')
            messages.error(request, 'Form jest niepoprawny.')

    lz = Lista_Zawodnikow.objects.all()
    paginator = Paginator(lz, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    ulz = LZForm()
    return render(request=request, template_name="lista_zawodnikow.html", context={"page_obj": page_obj, "ulz": ulz,
                                                                                   })


class crlista_zawodnikow(CreateView):
    model = Lista_Zawodnikow
    fields = 'Osoba', 'Zawody', 'Dyscyplina', 'Czas_Odleglosc'
    template_name = "dodaj.html"
    success_url = "/lista_zawodnikow/"


class uplista_zawodnikow(UpdateView):
    model = Lista_Zawodnikow
    fields = 'Osoba', 'Zawody', 'Dyscyplina', 'Czas_Odleglosc'
    template_name = 'dodaj.html'
    success_url = '/lista_zawodnikow/'


class delista_zawodnikow(DeleteView):
    model = Lista_Zawodnikow
    template_name = 'usun.html'
    success_url = '/lista_zawodnikow/'


def test(request):
    lz = Lista_Zawodnikow.objects.values_list('Zawody', 'Osoba', named=True).distinct()
    lz1 = Lista_Zawodnikow.objects.values_list('Zawody', flat=True)
    lz11 = Lista_Zawodnikow.objects.values_list('Osoba', flat=True)
    lz2 = Lista_Zawodnikow.objects.values_list('Zawody', 'Osoba', named=True)
    zawody = dict()
    osoby = list()
    x = Zawody.objects.filter(id__in=lz1)
    x1 = Osoba.objects.filter(id__in=lz11)
    lz3 = lz.intersection(lz, lz2)

    queryset = (Lista_Zawodnikow.objects.values('Zawody__zawody_nazwa').annotate(total=Count('Zawody')).order_by())
    qs = (Lista_Zawodnikow.objects.filter(Zawody__zawody_nazwa=queryset).values('Osoba__imie', 'Osoba__nazwisko').annotate(total=Count('Osoba')).order_by())
    # for i in lz3:
    #     osoby.clear()
    #     for k in i:
    #         osoby.append(k)
    #     zawody[i] = osoby
    b = Lista_Zawodnikow.objects.all().prefetch_related('Osoba').distinct()
    # zw = Zawody.objects.filter(pk__in=zawody)

    paginator = Paginator(lz, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request=request, template_name="test.html", context={"page_obj": page_obj, "lz": lz3, "z": zawody, "b": b, "x": x, "x1": x1, "queryset": queryset})
