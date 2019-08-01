from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import redirect
from .forms import TelefonForm, EmailForm, KontaktForm

from .models import Osoba, Telefon, Email

# Create your views here.
def index(request):
    osoba = Osoba.objects.order_by('nazwisko')[:]
    template = loader.get_template('kontakty/index.html')
    context = {
        'nazwiska': osoba,
    }
    return render(request, 'kontakty/index.html', context)

def edycja(request, k_id):
    osoba = get_object_or_404(Osoba, pk=k_id)
    if request.method == "POST":
        imi = request.POST.get('imie')
        naz = request.POST.get('nazwisko')
        tel = Telefon.objects.filter(osoba_id=k_id)
        ema = Email.objects.filter(osoba_id=k_id)
        a = Osoba.objects.filter(pk=k_id).update(imie=imi)
        a = Osoba.objects.filter(pk=k_id).update(nazwisko=naz)

        for e in tel:
            req = request.POST.get(str(e.pk))
            req2 = request.POST.get(str(e.pk)+'1')
            
            if req != req2 and req != "":
                a = Telefon.objects.filter(pk=e.pk, telefon = req2).update(telefon=req)
            if req == "":
                a = Telefon.objects.filter(pk=e.pk, telefon = req2).delete()
        for f in ema:
            emreq = request.POST.get(str(f.pk))
            emreq2 = request.POST.get(str(f.pk)+'1')

            if emreq != emreq2 and emreq != "":
                b = Email.objects.filter(pk=f.pk, email = emreq2).update(email=emreq)
            if emreq == "":
                b = Email.objects.filter(pk=f.pk, email = emreq2).delete()


        
        return redirect('/kontakty/')

    return render(request, 'kontakty/edycja.html', {'osoba': osoba})


def dodajnumer(request, k_id):
    osoba = get_object_or_404(Osoba, pk=k_id)
    if request.method == "POST":
        form = TelefonForm(request.POST)
        if form.is_valid():
            osoba = form.save(commit=False)
            osoba.osoba_id = k_id
            osoba.save()
            return redirect('/kontakty/')
    else:
        form = TelefonForm()
    return render(request, 'kontakty/dodajnumer.html', {'form': form, 'osoba':osoba})


def dodajmail(request, k_id):
    osoba = get_object_or_404(Osoba, pk=k_id)
    if request.method == "POST":
        form = EmailForm(request.POST)
        if form.is_valid():
            osoba = form.save(commit=False)
            osoba.osoba_id = k_id
            osoba.save()
            return redirect('/kontakty/')
    else:
        form = EmailForm()

    return render(request, 'kontakty/dodajmail.html', {'form': form, 'osoba':osoba})

def dodajkontakt(request):
   if request.method == "POST":
        form = KontaktForm(request.POST)
        tel = request.POST.get('telefon')
        ema = request.POST.get('email')
        if form.is_valid():
            osoba = form.save(commit=False)
            osoba.save()
            if tel != '':
                a = Telefon.objects.create(telefon=tel, osoba_id = osoba.id)
                a.save()
            if ema != '':
                a = Email.objects.create(email=ema, osoba_id = osoba.id)
                a.save()
            
            return redirect('/kontakty/')
   else:
        form = KontaktForm()

   return render(request, 'kontakty/dodajkontakt.html', {'form': form})

def szukaj(request):
    search_id = request.GET.get('search_box')
    osoba = []
    tel = []
    mail = []
    if ' ' not in search_id:
        osoba += Osoba.objects.filter(imie__icontains = search_id)
        osoba += Osoba.objects.filter(nazwisko__icontains = search_id)
        tel = Telefon.objects.filter(telefon__icontains = search_id)
        
        for n in tel:
            osoba += Osoba.objects.filter(pk = n.osoba_id)

        mail = Email.objects.filter(email__icontains = search_id)
        for n in mail:
            osoba += Osoba.objects.filter(pk = n.osoba_id)
    else:
        users = []
        firstname = search_id.split(' ')[0]
        lastname  = search_id.split(' ')[1]
        osoba += Osoba.objects.filter(imie__icontains=firstname,nazwisko__icontains=lastname)
        osoba += Osoba.objects.filter(imie__icontains=lastname,nazwisko__icontains=firstname)
        users = set(users)
    osoba = list(set(osoba))

    return render(request, 'kontakty/szukaj.html', {'osoba': osoba})     

def delete(request, id):
    u = get_object_or_404(Osoba, pk=id).delete()
    osoba = Osoba.objects.order_by('nazwisko')[:]
    template = loader.get_template('kontakty/index.html')
    context = {
        'nazwiska': osoba,
    }
    return redirect('/kontakty/', context)