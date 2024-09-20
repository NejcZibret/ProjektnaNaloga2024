import re
import html  
import os

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
    # ocena smučišča
    r'<tr>.*?(<div class="rating-list js-star-ranking stars-middle".*?data-rank="(?P<ocena>\d(\.\d)?)".*?)?</tr>.*?'
       
    # dolžina prog
    r'<td>\s*<span\s*class="slopeinfoitem\s*'
    r'active">(?P<skupna_dolzina>\d+(\.\d+)?)\skm</span>.*?(<span class="slopeinfoitem blue">(?P<dolzina_modrih>\d+(\.\d+)?)\skm</span>.*?)?'
    r'(<span class="slopeinfoitem red">(?P<dolzina_rdecih>\d+(\.\d+)?)\skm</span>.*?)?'
    r'(<span class="slopeinfoitem black">(?P<dolzina_crnih>\d+(\.\d+)?)\skm</span>.*?)?</td>',
    flags=re.DOTALL
)

# izločanje podatkov smučišča
def izloci_podatke_smucisca(blok):
    najdba = vzorec_smučišča.search(blok) # to je prvi match
    smucisce = najdba.groupdict() # vrne slovar vseh vzorcev, poimenovanih zgoraj
    
    smucisce['mesto_po_velikosti'] = int(smucisce['mesto_po_velikosti'])
    smucisce['ime'] = pocisti_imena_smucisc(smucisce['ime'])
    smucisce['celina'] = pocisti_celine_in_drzave(smucisce['celina'])
    smucisce['drzava'] = pocisti_celine_in_drzave(smucisce['drzava']) if smucisce['drzava'] not in (None, '') else 'Country is not provided.'
    smucisce['ocena'] = float(smucisce['ocena']) if smucisce['ocena'] not in (None, '') else 'There is no rating.'
    smucisce['skupna_dolzina'] = float(smucisce['skupna_dolzina'])
    smucisce['dolzina_modrih'] = float(smucisce['dolzina_modrih']) if smucisce['dolzina_modrih'] not in (None, '') else 'Not known.'
    smucisce['dolzina_rdecih'] = float(smucisce['dolzina_rdecih']) if smucisce['dolzina_rdecih'] not in (None, '') else 'Not known.'
    smucisce['dolzina_crnih'] = float(smucisce['dolzina_crnih']) if smucisce['dolzina_crnih'] not in (None, '') else 'Not known.'

    return smucisce

# izločanje vseh smučišč s strani
def izloci_vsa_smucisca(vsebina):
    bloki = vzorec_bloka.findall(vsebina)
    seznam_smucisc = []
    # iz vsakega bloka izločim ime, dodam v seznam_smucisc
    for blok in bloki:
        pociscen_blok = izloci_podatke_smucisca(blok)
        seznam_smucisc.append(pociscen_blok)
    return seznam_smucisc

seznam_smucisc = []
for i in range(1, 17):
    with open(os.path.join('smucisca', f'smucisca{i}.html'), 'r', encoding='utf-8') as f:
        stran = f.read()
    smucisca_iz_datoteke = izloci_vsa_smucisca(stran)
    seznam_smucisc.extend(smucisca_iz_datoteke)

# izpišem seznam smučišč
print(f"Najdena smučišča: {seznam_smucisc}")
print(f'Vseh smučišč je: {len(seznam_smucisc)}')







import csv
import json
import os
import requests
import sys
import html
import re

def pripravi_imenik(ime_datoteke):
    '''če še ne obstaja, pripravi prazen imenik za dano datoteko'''
    imenik = os.path.dirname(ime_datoteke)
    if imenik:
        os.makedirs(imenik, exist_ok=True)

def shrani_spletno_stran(url, ime_datoteke, vsili_prenos=False):
    '''Vsebino strani na danem naslovu shrani v datoteko z danim imenom.'''
    try:
        print(f'Shranjujem {url} ...', end='')
        sys.stdout.flush()
        if os.path.isfile(ime_datoteke) and not vsili_prenos:
            print('Shranjeno že od prej!')
            return
        r = requests.get(url)
        r.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f'Napaka pri prenosu: {e}')
    else:
        pripravi_imenik(ime_datoteke)
        with open(ime_datoteke, 'w', encoding='utf-8') as datoteka:
            datoteka.write(r.text)
            print('Shranjeno!')

def vsebina_datoteke(ime_datoteke):
    '''Vrne niz z vsebino datoteke z danim imenom.'''
    with open(ime_datoteke, encoding='utf-8') as datoteka:
        return datoteka.read()

# Ustvari imenik za shranjevanje HTML datotek
if not os.path.exists('smucisca'):
    os.makedirs('smucisca')

# Prenos HTML strani
for i in range(1, 27):
    if i == 1:
        url = 'https://www.skiresort.info/ski-resorts/sorted/slope-length/'
    else:
        url = f'https://www.skiresort.info/ski-resorts/page/{i}/sorted/slope-length/'

    ime_datoteke = os.path.join('smucisca', f'smucisca{i}.html')
    
    # Shranjevanje strani
    shrani_spletno_stran(url, ime_datoteke)

# Dodajanje funkcij za zapis v CSV in JSON
def zapisi_csv(slovarji, imena_polj, ime_datoteke):
    '''Iz seznama slovarjev ustvari CSV datoteko z glavo.'''
    pripravi_imenik(ime_datoteke)
    with open(ime_datoteke, 'w', encoding='utf-8', newline='') as csv_datoteka:
        writer = csv.DictWriter(csv_datoteka, fieldnames=imena_polj)
        writer.writeheader()
        writer.writerows(slovarji)

def zapisi_json(objekt, ime_datoteke):
    '''Iz danega objekta ustvari JSON datoteko.'''
    pripravi_imenik(ime_datoteke)
    with open(ime_datoteke, 'w', encoding='utf-8') as json_datoteka:
        json.dump(objekt, json_datoteka, indent=4, ensure_ascii=False)

# Dodajanje kode za obdelavo HTML in shranjevanje podatkov
# ... (tu dodaj obstoječo kodo za obdelavo HTML in shranjevanje v CSV/JSON)







import re
import os
import html
import requests

if not os.path.exists('smucisca'):
    os.makedirs('smucisca')

for i in range(1, 27):
    if i == 1:
        url = 'https://www.skiresort.info/ski-resorts/sorted/slope-length/'
    else:
        url = f'https://www.skiresort.info/ski-resorts/page/{i}/sorted/slope-length/'

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
    }

    try:
        odziv = requests.get(url, headers=headers)
        odziv.raise_for_status()  

        if odziv.status_code == 200:
            print(f"Uspeh: {url}")
            # Shrani HTML vsebino v datoteko
            ime_datoteke = f'stran-{i}.html'
            with open(os.path.join('smucisca', f'smucisca{i}.html'), 'w', encoding='utf-8') as dat:
                dat.write(odziv.text)
        else:
            print(f"Nepričakovana koda statusa {odziv.status_code} za {url}")

    except requests.exceptions.RequestException as e:
        print(f"Prišlo je do napake: {e}")


def pocisti_imena_smucisc(niz):
    # Najprej odstrani span elemente, ki označujejo začasno zaprta smučišča
    pocisceno_ime = re.sub(r'<span class="closed-resort red">.*?</span>', '', niz)
    
    # Nato ostala čiščenja
    pocisceno_ime = html.unescape(pocisceno_ime).strip() 
    pocisceno_ime = re.sub(r'\s+', ' ', pocisceno_ime)  # kjer je več presledkov, dam enega
    pocisceno_ime = re.sub(r'\u200b', '', pocisceno_ime)  # odstrani 'zero-width space' znake
    return pocisceno_ime

def poisci(i):
    with open(os.path.join('smucisca', f'smucisca{i}.html'), encoding='utf-8') as dat:
        besedilo = dat.read()
        niz = r'<a class="h3"\s*href=".*?">\s*\d*\.\s*(?P<ime>.*?)</a>'
        smucisca = []
        for najdba in re.finditer(niz, besedilo, re.DOTALL):
            smucisca.append(najdba.group('ime'))

        cista_smucisca = [pocisti_imena_smucisc(s) for s in smucisca]
        return cista_smucisca

# Glavni del
vsa_smucisca = []

for i in range(1, 27):
    vsa_smucisca.extend(poisci(i))

print(vsa_smucisca)
print(len(vsa_smucisca))








import csv
import json
import os
import requests
import sys


def pripravi_imenik(ime_datoteke):
    '''če še ne obstaja, pripravi prazen imenik za dano datoteko'''
    imenik = os.path.dirname(ime_datoteke)
    if imenik:
        os.makedirs(imenik, exist_ok=True)
        


def shrani_spletno_stran(url, ime_datoteke, vsili_prenos=False):
    '''Vsebino strani na danem naslovu shrani v datoteko z danim imenom.'''
    try:
        print(f'Shranjujem {url} ...', end='')
        sys.stdout.flush()
        if os.path.isfile(ime_datoteke) and not vsili_prenos:
            print('Shranjeno že od prej!')
            return
        r = requests.get(url)
    except requests.exceptions.ConnectionError:
        print('Stran ne obstaja!')
    else:
        pripravi_imenik(ime_datoteke)
        with open(ime_datoteke, 'w', encoding='utf-8') as datoteka:
            datoteka.write(r.text)
            print('Shranjeno!')

def vsebina_datoteke(ime_datoteke):
    '''Vrne niz z vsebino datoteke z danim imenom.'''
    with open(ime_datoteke, encoding='utf-8') as datoteka:
        return datoteka.read()
    

def zapisi_csv(slovarji, imena_polj, ime_datoteke):
    '''Iz seznama slovarjev ustvari CSV datoteko z glavo.'''
    pripravi_imenik(ime_datoteke)
    with open(ime_datoteke, 'w', encoding='utf-8') as csv_datoteka:
        writer = csv.DictWriter(csv_datoteka, fieldnames=imena_polj)
        writer.writeheader()
        writer.writerows(slovarji)
        
def zapisi_json(objekt, ime_datoteke):
    '''Iz danega objekta ustvari JSON datoteko'''
    pripravi_imenik(ime_datoteke)
    with open(ime_datoteke, 'w', encoding='utf-8') as json_datoteka:
        json.dump(objekt, json_datoteka, indent=4, ensure_ascii=False)








import re
import os


import requests
import os
import time

if not os.path.exists('smucisca'):
    os.makedirs('smucisca')

for i in range(1, 33):
    if i == 1:
        url = 'https://www.skiresort.info/ski-resorts/sorted/slope-length/'
    else:
        url = f'https://www.skiresort.info/ski-resorts/page/{i}/sorted/slope-length/'

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
    }

    try:
        odziv = requests.get(url, headers=headers)
        odziv.raise_for_status()  

        if odziv.status_code == 200:
            print(f"Uspeh: {url}")
            # Shrani HTML vsebino v datoteko
            ime_datoteke = f'stran-{i}.html'
            with open(os.path.join('smucisca', f'smucisca{i}.html'), 'w', encoding='utf-8') as dat:
                dat.write(odziv.text)
        else:
            print(f"Nepričakovana koda statusa {odziv.status_code} za {url}")

    except requests.exceptions.RequestException as e:
        print(f"Prišlo je do napake: {e}")


import re
import os
import html

def pocisti_imena_smucisc(niz):
    pocisceno_ime = html.unescape(niz).strip() 
    pocisceno_ime = re.sub(r'\s+', ' ', pocisceno_ime)  # kjer je več presledkov, dam enega
    pocisceno_ime = re.sub(r'\u200b', '', pocisceno_ime)  # odstrani 'zero-width space' znake
    return pocisceno_ime

def poisci(i):
    with open(os.path.join('smucisca', f'smucisca{i}.html'), encoding='utf-8') as dat:
        besedilo = dat.read()
        niz = r'<a class="h3"\s*href=".*?">\s*\d*\.\s*(?P<ime>.*?)</a>'
        smucisca = []
        for najdba v re.finditer(niz, besedilo, re.DOTALL):
            smucisca.append(najdba.group('ime'))
        
        cista_smucisca = [pocisti_imena_smucisc(s) for s in smucisca]
        return cista_smucisca

# Glavni del
vsa_smucisca = []  # Skupni seznam, kamor bomo shranjevali vsa smučišča

for i in range(1, 33):
    vsa_smucisca.extend(poisci(i))  # Dodaj vsako smučišče v skupni seznam

# Natisni skupni seznam vseh smučišč
print(vsa_smucisca)


vzorec_bloka = re.compile(
    r'<div class="panel panel-default resort-list-item resort-list-item-image--big"'  # Začetek bloka smučišča
    r'.*?'
    r'</div>\s*</div>\s*</div>',  # Konec bloka smučišča
    flags=re.DOTALL
)






import requests
import os
import time

if not os.path.exists('smucisca'):
    os.makedirs('smucisca')

for i in range(1, 33):
    if i == 1:
        url = 'https://www.skiresort.info/ski-resorts/sorted/slope-length/'
    else:
        url = f'https://www.skiresort.info/ski-resorts/page/{i}/sorted/slope-length/'

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
    }

    try:
        odziv = requests.get(url, headers=headers)
        odziv.raise_for_status()  

        if odziv.status_code == 200:
            print(f"Uspeh: {url}")
            # Shrani HTML vsebino v datoteko
            ime_datoteke = f'stran-{i}.html'
            with open(os.path.join('smucisca', f'smucisca{i}.html'), 'w', encoding='utf-8') as dat:
                dat.write(odziv.text)
        else:
            print(f"Nepričakovana koda statusa {odziv.status_code} za {url}")

    except requests.exceptions.RequestException as e:
        print(f"Prišlo je do napake: {e}")