import re
import html  
import os




# pomožna funkcija 1
def pocisti_imena_smucisc(niz):
    pocisceno_ime = re.sub(r'<span class=".*?">.*?</span>', '', niz)
    pocisceno_ime = html.unescape(pocisceno_ime).strip() 
    pocisceno_ime = re.sub(r'\s+', ' ', pocisceno_ime)  
    pocisceno_ime = re.sub(r'\u200b', '', pocisceno_ime)
    return pocisceno_ime

# pomožna funkcija 2
def pocisti_celine_in_drzave(niz):
    pocisceno_ime = html.unescape(niz).strip()
    pocisceno_ime = re.sub(r'\s+', ' ', pocisceno_ime)  
    pocisceno_ime = re.sub(r'\u200b', '', pocisceno_ime)
    return pocisceno_ime




# blok smučišča
vzorec_bloka = re.compile(
    r'<div class="panel panel-default resort-list-item resort-list-item-image--big"'  # Začetek bloka smučišča
    r'.*?'
    r'<div class=".*?"><a class=".*?"\s*href=".*?">\s*Details\s*</a>\s*</div>\s*</div>\s*</div>',  # Konec bloka smučišča
    flags=re.DOTALL
)


# natančnejša obdelava 
vzorec_smučišča = re.compile(
    # ime smučišča ter mesto, na katerem se nahaja po velikosti
    r'<a class="h3"\s*href=".*?">\s*(?P<mesto_po_velikosti>\d+)\.\s+(?P<ime>.*?)</a>.*?'
    # celina in država
    r'<div class="sub-breadcrumb">\s*<div\s*class="\s*sub-breadcrumb">\s*<a\s*href=".*?">(?P<celina>.*?)</a>\s*<a\s*href=".*?">(?P<drzava>.*?)</a>.*?'
    # ocena smučišča
    r'<div\s*class="\s*rating-list\s+js-star-ranking\s+stars-middle".*?data-rank="(?P<ocena>\d(\.\d)?)".*?'
    # višinska razlika
    r'<td>\s*<span>(?P<visinska_razlika>\d+(\.\d)?)\s+m</span>.*?'
    # dolžina rdečih prog
    r'<span\s*class="slopeinfoitem\s+red">\s*(?P<dolzina_rdecih_prog>\d+(\.\d)?)\s*km\s*</span>.*?'
    # dolžina črnih prog
    r'<span\s*class="slopeinfoitem\s+black">\s*(?P<dolzina_crnih_prog>\d+(\.\d)?)\skm\s*</span>.*?'
    # število žičnic
    r'<li>\s*(?P<stevilo_zicnic>\d+)\s*ski\s*lifts\s*</li>.*?',
    flags=re.DOTALL
)


# izločanje podatkov smučišča
def izloci_podatke_smucisca(blok):
    najdba = vzorec_smučišča.search(blok) # to je prvi match
    smucisce = najdba.groupdict() # vrne slovar vseh vzorcev, poimenovanih zgoraj
    
    smucisce['mesto_po_velikosti'] = int(smucisce['mesto_po_velikosti'])
    smucisce['ime'] = pocisti_celine_in_drzave(smucisce['ime'])
    smucisce['celina'] = pocisti_celine_in_drzave(smucisce['celina'])
    smucisce['ocena'] = float(smucisce['ocena'])
    smucisce['visinska_razlika'] = int(smucisce['visinska_razlika'])
    smucisce['stevilo_zicnic'] = int(smucisce['stevilo_zicnic']) 
    smucisce['dolzina_rdecih_prog'] = float(smucisce['dolzina_rdecih_prog'])
    smucisce['dolzina_crnih_prog'] = float(smucisce['dolzina_crnih_prog'])
    
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
for i in range(1, 3):
    with open(os.path.join('smucisca', f'smucisca{i}.html'), 'r', encoding='utf-8') as f:
        stran = f.read()
    smucisca_iz_datoteke = izloci_vsa_smucisca(stran)
    seznam_smucisc.extend(smucisca_iz_datoteke)


# izpišem seznam smučišč
print(f"Najdena smučišča: {seznam_smucisc}")
print(f'Vseh smučišč je: {len(seznam_smucisc)}')

