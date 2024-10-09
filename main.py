import csv
import json
import os
import requests
import sys
import html
import re
import numpy as np



# 1. DEL: HTML DATOTEKE
# Pri prvem delu sem si pomagal z datoteko profesorja Matije Pretnarja orodja.py (uporabil jo je pri predmetu programiranje 1), s katero 
# sem pridobil toliko strani, da sem dobil podatke o 3850 smučiščih, če ti že niso bili predhodno pridobljeni.


def pripravi_imenik(ime_datoteke):
    '''če še ne obstaja, pripravi prazen imenik za dano datoteko'''
    imenik = os.path.dirname(ime_datoteke)
    if imenik:
        os.makedirs(imenik, exist_ok=True)
        
        
def shrani_spletno_stran(url, ime_datoteke, vsili_prenos=False):
    '''Vsebino strani na danem naslovu shrani v datoteko z danim imenom.'''
    try:
        print(f'Shranjujem {url} ...', end='')
        sys.stdout.flush()  # ukaz se takoj prikaže na konzoli 
        if os.path.isfile(ime_datoteke) and not vsili_prenos:
            print(' Shranjeno že od prej!')
            return
        r = requests.get(url)
        r.raise_for_status()
    except requests.exceptions.ConnectionError:
        print(f'Stran ne obstaja!')
    else:
        pripravi_imenik(ime_datoteke)
        with open(ime_datoteke, 'w', encoding='utf-8') as datoteka:
            datoteka.write(r.text)
            print(' Shranjeno!')


def vsebina_datoteke(ime_datoteke):
    '''Prebere vsebino datoteke.'''
    with open(ime_datoteke, encoding='utf-8') as datoteka:
        return datoteka.read()
    

if not os.path.exists('smucisca'):
    '''Ustvari pot, če ta še ne obstaja.'''
    os.makedirs('smucisca')
    

for i in range(1, 21):
    '''Sedaj uporabimo vse zgoraj, shranimo spletne strani v mapo smucisca.'''
    if i == 1:
        url = 'https://www.skiresort.info/ski-resorts/sorted/slope-length/'
    else:
        url = f'https://www.skiresort.info/ski-resorts/page/{i}/sorted/slope-length/'

    ime_datoteke = os.path.join('smucisca', f'smucisca{i}.html')
    
    # Shranjevanje strani
    shrani_spletno_stran(url, ime_datoteke)
    



# 2. DEL: FUNKCIJE Z UPORABO RE
# Tukaj sem najprej poiskal blok ter znotraj bloka nato iskal podrobneje vse podatke, ki sem jih želel zajeti pri moji analizi.
# Tudi tu sem si pomagal s posnetki profesorja Pretnarja.


# pomožna funkcija 1
def pocisti_imena_smucisc(niz):
    pocisceno_ime = re.sub(r'\s+', ' ', niz) 
    pocisceno_ime = html.unescape(pocisceno_ime).strip()  
    pocisceno_ime = re.sub(r'\u200b', '', pocisceno_ime)  
    pocisceno_ime = re.sub(r'<.*?>', '', pocisceno_ime)
    return pocisceno_ime


# pomožna funkcija 2
def pocisti_celine_in_drzave(niz):
    pocisceno_ime = re.sub(r'\s*<span\s*class="closed-resort\s+\w+">\s*', '', niz)
    pocisceno_ime = re.sub(r'\u200b', '', pocisceno_ime)
    pocisceno_ime = html.unescape(pocisceno_ime).strip()
    pocisceno_ime = re.sub(r'\s+', ' ', pocisceno_ime)  
    return pocisceno_ime


# blok smučišča
vzorec_bloka = re.compile(
    r'<div class="panel panel-default resort-list-item resort-list-item-image--big"'  # Začetek bloka smučišča
    r'.*?'
    r'<div\s*class=".*?">\s*<a\s+class=".*?"\s+href=".*?">\s*Details\s*</a>\s*</div>\s*</div>\s*</div>',  # Konec bloka smučišča
    flags=re.DOTALL
)


# natančnejša obdelava 
vzorec_smučišča = re.compile(
    # ime smučišča ter mesto, na katerem se nahaja po velikosti
    r'<a\s+class="h3"\s+href=".*?">\s*(?P<mesto_po_velikosti>\d+)\.\s+(?P<ime>.*?)\s*</a>.*?'
    
    # celina in država
    r'<div\s+class="sub-breadcrumb">\s*<a\s+href=".*?">(?P<celina>.*?)</a>\s*(<a\s+href=".*?">\s*(?P<drzava>.*?)</a>)?.*?'
    
    # ocena smučišča in višinska razlika
    r'<tbody>\s*<tr>.*?(<div class="rating-list js-star-ranking stars-middle".*?data-rank="(?P<ocena>\d(\.\d)?)".*?)?</tr>(\s*<tr>.*?<td><span>'
    r'(?P<visinska_razlika>\d+(\.\d)?) m</span>.*?</tr>)?.*?'
       
    # dolžina prog in število žičnic
    r'<td>\s*<span\s*class="slopeinfoitem\s*'
    r'active">(?P<skupna_dolzina>\d+(\.\d+)?)\skm</span>.*?(<span class="slopeinfoitem blue">(?P<dolzina_modrih>\d+(\.\d+)?)\skm</span>.*?)?'
    r'(<span class="slopeinfoitem red">(?P<dolzina_rdecih>\d+(\.\d+)?)\skm</span>.*?)?'
    r'(<span class="slopeinfoitem black">(?P<dolzina_crnih>\d+(\.\d+)?)\skm</span>.*?)?</td>'
    r'(.*?<td>.*?</td>\s*<td>\s*<ul class="inline-dot">\s*<li>(?P<stevilo_zicnic>\d*)&nbsp;ski lifts</li>.*?)?\s*</tr>\s*</tbody>',
    flags=re.DOTALL
)


# izločanje podatkov smučišča
def izloci_podatke_smucisca(blok):
    najdba = vzorec_smučišča.search(blok) 
    smucisce = najdba.groupdict() # vrne slovar vseh vzorcev, poimenovanih v regularnih izrazih zgoraj
    
    smucisce['mesto_po_velikosti'] = int(smucisce['mesto_po_velikosti'])
    smucisce['ime'] = pocisti_imena_smucisc(smucisce['ime'])
    smucisce['celina'] = pocisti_celine_in_drzave(smucisce['celina'])
    if smucisce['celina'] == 'Russia':
        if smucisce['drzava'] in ['Ural Federal District', 'Southern Russia', 'Northwest Russia', 'North Caucasus', 'Volga Federal District', 'Central Russia']:
            smucisce['celina'] = 'Europe'
            smucisce['drzava'] = 'Russia'
        else:
            smucisce['celina'] = 'Asia'
            smucisce['drzava'] = 'Russia'

    smucisce['drzava'] = pocisti_celine_in_drzave(smucisce['drzava']) if smucisce['drzava'] not in (None, '') else 'no data'
    smucisce['ocena'] = float(smucisce['ocena']) if smucisce['ocena'] not in (None, '') else np.nan
    smucisce['visinska_razlika'] = float(smucisce['visinska_razlika']) if smucisce['visinska_razlika'] not in (None, '') else np.nan
    smucisce['skupna_dolzina'] = float(smucisce['skupna_dolzina'])
    smucisce['dolzina_modrih'] = float(smucisce['dolzina_modrih']) if smucisce['dolzina_modrih'] not in (None, '') else np.nan
    smucisce['dolzina_rdecih'] = float(smucisce['dolzina_rdecih']) if smucisce['dolzina_rdecih'] not in (None, '') else np.nan
    smucisce['dolzina_crnih'] = float(smucisce['dolzina_crnih']) if smucisce['dolzina_crnih'] not in (None, '') else np.nan
    smucisce['stevilo_zicnic'] = int(smucisce['stevilo_zicnic']) if smucisce['stevilo_zicnic'] not in (None, '') else np.nan
    return smucisce


# izločanje vseh smučišč s strani
def izloci_vsa_smucisca(vsebina):
    bloki = vzorec_bloka.findall(vsebina)
    lokalni_seznam_smucisc = []
    # iz vsakega bloka izločim ime, dodam v seznam_smucisc
    for blok in bloki:
        pociscen_blok = izloci_podatke_smucisca(blok)
        lokalni_seznam_smucisc.append(pociscen_blok)
    return lokalni_seznam_smucisc


seznam_smucisc = []
for i in range(1, 21):
    with open(os.path.join('smucisca', f'smucisca{i}.html'), 'r', encoding='utf-8') as f:
        stran = f.read()
    smucisca_iz_datoteke = izloci_vsa_smucisca(stran)
    seznam_smucisc.extend(smucisca_iz_datoteke)




# 3. DEL: CSV
# Iz vseh podatkov sem tukaj naredil najprej json, nato še csv datoteko. 


# zapišem json, dodam zamike in zagotovim pravilen prikaz črk različnih jezikov
with open('smucisca.json', 'w', encoding='utf-8') as f:
    json.dump(seznam_smucisc, f, ensure_ascii=False, indent=4)
    
    
# napišem csv datoteko
with open('smucisca.csv', 'w', encoding='utf-8-sig', newline='') as f:
    pisatelj = csv.writer(f)
    pisatelj.writerow(['položaj', 'ime', 'celina', 'država', 'ocena', 'višinska_razlika', 'proge', 'modre', 'rdeče', 'črne', 'žičnice'])
    for smucisce in seznam_smucisc:
        položaj = smucisce['mesto_po_velikosti']
        ime = smucisce['ime']
        celina = smucisce['celina']
        država = smucisce['drzava']
        ocena = smucisce['ocena']
        višinska_razlika = smucisce['visinska_razlika']
        proge = smucisce['skupna_dolzina']
        modre = smucisce['dolzina_modrih']
        rdeče = smucisce['dolzina_rdecih']
        črne = smucisce['dolzina_crnih']
        žičnice = smucisce['stevilo_zicnic']
        pisatelj.writerow([položaj, ime, celina, država, ocena, višinska_razlika, proge, modre, rdeče, črne, žičnice])
        

# preverim, ali deluje pravilno
print(f'Vseh smučišč je: {len(seznam_smucisc)}')

        

