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

