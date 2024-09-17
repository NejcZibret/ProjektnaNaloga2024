import re

vzorec_bloka = re.compile(
    r'<div class="panel panel-default resort-list-item resort-list-item-image--big".*?</div>\s*</div>\s*</div>',
    flags=re.DOTALL
)

vzorec_smučišča = re.compile(
    # ime smučišča
    r'<a class="h3"\s*href="[^"]*">\s*\d*\.\s*(?P<ime>.*?)</a>.*?'
    # celina in država
    r'<div class="sub-breadcrumb">.*?<a\s*href="[^"]*">(?P<celina>.*?)</a>\s*<a\s*href="[^"]*">(?P<drzava>.*?)</a>.*?'
    # ocena smučišča
    r'<div class="star-wrap stars-middle-grey rating-list".*?data-rank="(?P<ocena>\d+(\.\d+)?)".*?'
    # višinska razlika
    r'<td><span>(?P<visinska_razlika>\d+(\.\d+)?)\sm</span>.*?'
    # skupna dolžina
    r'<td><span class="slopeinfoitem active">(?P<skupna_dolzina>\d+(\.\d+)?)\skm</span>.*?'
    # dolžina modrih prog
    r'<span class="slopeinfoitem blue">(?P<dolzina_modrih>\d+(\.\d+)?)\skm</span>.*?'
    # dolžina rdečih prog
    r'<span class="slopeinfoitem red">(?P<dolzina_rdecih>\d+(\.\d+)?)\skm</span>.*?'
    # dolžina črnih prog
    r'<span class="slopeinfoitem black">(?P<dolzina_crnih>\d+(\.\d+)?)\skm</span>.*?'
    # število žičnic
    r'<li>(?P<stevilo_zicnic>\d+)\sski\slifts</li>.*?',
    flags=re.DOTALL
)

def izloci_podatke_smucisca(blok):
    smucisce = vzorec_smučišča.search(blok).groupdict()
    smucisce['ime'] = smucisce['ime'].strip()  
    smucisce['celina'] = smucisce['celina'].strip()  
    smucisce['drzava'] = smucisce['drzava'].strip()  
    smucisce['ocena'] = float(smucisce['ocena'])  
    smucisce['visinska_razlika'] = float(smucisce['visinska_razlika'])  # Višinska razlika (število v metrih)
    smucisce['skupna_dolzina'] = float(smucisce['skupna_dolzina'])  # Skupna dolžina prog (število v km)
    smucisce['dolzina_modrih'] = float(smucisce['dolzina_modrih'])  # Dolžina modrih prog (število v km)
    smucisce['dolzina_rdecih'] = float(smucisce['dolzina_rdecih'])  # Dolžina rdečih prog (število v km)
    smucisce['dolzina_crnih'] = float(smucisce['dolzina_crnih'])  # Dolžina črnih prog (število v km)
    smucisce['stevilo_zicnic'] = int(smucisce['stevilo_zicnic'])  # Število žičnic (število)
    return smucisce


def prestej_ponovitve(vsebina):
    ujemanja = vzorec_bloka.findall(vsebina)
    stevec = len(ujemanja)
    return stevec

with open('html_primer.html', 'r', encoding='utf-8') as f:
    stran = f.read()

stevilo_blokov = prestej_ponovitve(stran)
print(f"Število smučišč: {stevilo_blokov}")

