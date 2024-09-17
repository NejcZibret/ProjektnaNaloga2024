import re
import html
import os

# pomožna funkcija 1: Čiščenje imen smučišč
def pocisti_imena_smucisc(niz):
    pocisceno_ime = re.sub(r'<span class=".*?">.*?</span>', '', niz)
    pocisceno_ime = html.unescape(pocisceno_ime).strip() 
    pocisceno_ime = re.sub(r'\s+', ' ', pocisceno_ime)  
    pocisceno_ime = re.sub(r'\u200b', '', pocisceno_ime)
    return pocisceno_ime

# pomožna funkcija 2: Čiščenje celine in države
def pocisti_celine_in_drzave(niz):
    pocisceno_ime = html.unescape(niz).strip()
    pocisceno_ime = re.sub(r'\s+', ' ', pocisceno_ime)  
    pocisceno_ime = re.sub(r'\u200b', '', pocisceno_ime)
    return pocisceno_ime

# Regularni izraz za identifikacijo posameznih blokov smučišč
vzorec_bloka = re.compile(
    r'<div class="panel\s*panel-default\s*resort-list-item\s*resort-list-item-image--big"'  # Začetek bloka smučišča
    r'.*?'
    r'<div class=".*?"><a\s*class=".*?"\s*href=".*?">\s*Details\s*</a>\s*</div>\s*</div>\s*</div>',  # Konec bloka smučišča
    flags=re.DOTALL
)

# Regularni izraz za identifikacijo podatkov v posameznem bloku smučišča
vzorec_smučišča = re.compile(
    # ime smučišča in mesto
    r'<a\s*class="h3"\s*href=".*?">\s*(?P<mesto_po_velikosti>\d*)\.\s*(?P<ime>.*?)</a>.*?'
    # celina in država
    r'<div\s*class="sub-breadcrumb">\s*<a\s*href=".*?">(?P<celina>.*?)</a>\s*<a\s*href=".*?">(?P<drzava>.*?)</a>.*?'
    # ocena smučišča
    r'<div\s*class="rating-list\s*js-star-ranking\s*stars-middle".*?data-rank="(?P<ocena>\d(\.\d)?)".*?'
    # višinska razlika
    r'<td><span>(?P<visinska_razlika>\d+(\.\d)?)\s*m</span>.*?'
    # dolžina rdečih prog
    r'<span\s*class="slopeinfoitem\s*red">(?P<dolzina_rdecih_prog>\d*(\.\d)?)\s*km</span>.*?'
    # dolžina črnih prog
    r'<span\s*class="slopeinfoitem\s*black">(?P<dolzina_crnih_prog>\d*(\.\d)?)\s*km</span>.*?'
    # število žičnic
    r'<li>(?P<stevilo_zicnic>\d*)\s*ski\slifts</li>.*?',
    flags=re.DOTALL
)

# Funkcija za izločanje podatkov o smučišču iz posameznega bloka
def izloci_podatke_smucisca(blok):
    najdba = vzorec_smučišča.search(blok)  # Poišče ujemanje v bloku
    if not najdba:
        return None  # Če ni ujemanja, vrne None
    smucisce = najdba.groupdict()  # Slovar z vsemi poimenovanimi podatki
    smucisce['mesto_po_velikosti'] = int(smucisce['mesto_po_velikosti'])  # Pretvorba v int
    smucisce['ime'] = pocisti_imena_smucisc(smucisce['ime'])
    smucisce['celina'] = pocisti_celine_in_drzave(smucisce['celina'])
    smucisce['drzava'] = pocisti_celine_in_drzave(smucisce['drzava'])
    smucisce['ocena'] = float(smucisce['ocena'])  # Pretvorba v float
    smucisce['visinska_razlika'] = int(smucisce['visinska_razlika'])  # Pretvorba v int
    smucisce['dolzina_rdecih_prog'] = float(smucisce['dolzina_rdecih_prog'])  # Pretvorba v float
    smucisce['dolzina_crnih_prog'] = float(smucisce['dolzina_crnih_prog'])  # Pretvorba v float
    smucisce['stevilo_zicnic'] = int(smucisce['stevilo_zicnic'])  # Pretvorba v int
    
    return smucisce

# Funkcija za izločanje vseh smučišč iz celotne vsebine HTML
def izloci_vsa_smucisca(vsebina):
    bloki = vzorec_bloka.findall(vsebina)  # Najde vse bloke smučišč
    seznam_smucisc = []
    for blok in bloki:
        smucisce = izloci_podatke_smucisca(blok)
        if smucisce:
            seznam_smucisc.append(smucisce)
    return seznam_smucisc

# Branje in izločanje smučišč iz več datotek
seznam_smucisc = []
for i in range(1, 5):  # Predpostavka, da imamo datoteke smucisca1.html do smucisca19.html
    try:
        with open(os.path.join('smucisca', f'smucisca{i}.html'), 'r', encoding='utf-8') as f:
            stran = f.read()
        smucisca_iz_datoteke = izloci_vsa_smucisca(stran)
        seznam_smucisc.extend(smucisca_iz_datoteke)  # Dodamo smučišča iz trenutne datoteke na seznam
    except FileNotFoundError:
        print(f"Datoteka smucisca{i}.html ni bila najdena.")
    except Exception as e:
        print(f"Napaka pri obdelavi datoteke smucisca{i}.html: {e}")

# Izpis celotnega seznama smučišč
print(f"Najdena smučišča: {seznam_smucisc}")
print(f'Vseh smučišč je: {len(seznam_smucisc)}')



