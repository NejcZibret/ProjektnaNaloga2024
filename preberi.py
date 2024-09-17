import re



vzorec_bloka = re.compile(
    r'<div class="panel panel-default resort-list-item resort-list-item-image--big"'  # Začetek bloka smučišča
    r'.*?'
    r'</div>\s*</div>\s*</div>',  # Konec bloka smučišča
    flags=re.DOTALL
)

vzorec_smučišča = re.compile(
    # ime smučišča
    r'<a class="h3"\s*href=".*?">\s*\d*\.\s*(?P<ime>.*?)</a>.*?'
    # celina in država
    r'<div class="sub-breadcrumb"><a\s*href=".*?">(?P<celina>.+?)</a>\s*<a href=".*?">(?P<drzava>.+?)</a>.*?'
    # ocena smučišča
    r'<div class=" star-wrap stars-middle-grey rating-list".*?data-rank="(?P<ocena>\d(\.\d)?)".*?'
    # višinska razlika
    r'<td><span>(?P<visinska_razlika>\d+(\.\d)?)\sm</span>.*?'
    # skupna dolžina
    r'<td><span class="slopeinfoitem active">(?P<skupna_dolzina>\d+(\.\d)?)\skm</span>.*?'
    # dolžina modrih prog
    r'<span class="slopeinfoitem blue">(?P<dolzina_modrih>\d+(\.\d)?)\skm</span>.*?'
    # dolžina rdečih prog
    r'<span class="slopeinfoitem red">(?P<dolzina_rdecih>\d+(\.\d)?)\skm</span>.*?'
    # dolžina črnih prog
    r'<span class="slopeinfoitem black">(?P<dolzina_crnih>\d+(\.\d)?)\skm</span>.*?'
    # število žičnic
    r'<li>(?P<stevilo_zicnic>\d+)\sski\slifts</li>.*?',
    flags=re.DOTALL
)

def izloci_podatke_smucisca(blok):
    smucisce = vzorec_smučišča.search(blok).groupdict()
    smucisce['ime'] = smucisce['ime'].strip()  # Ime smučišča (niz)
    smucisce['celina'] = smucisce['celina'].strip()  # Celina (niz)
    smucisce['drzava'] = smucisce['drzava'].strip()  # Država (niz)
    smucisce['ocena'] = float(smucisce['ocena'])  # Ocena (decimalno število)
    smucisce['visinska_razlika'] = int(smucisce['visinska_razlika'])  # Višinska razlika (število v metrih)
    smucisce['skupna_dolzina'] = int(smucisce['skupna_dolzina'])  # Skupna dolžina prog (število v km)
    smucisce['dolzina_modrih'] = int(smucisce['dolzina_modrih'])  # Dolžina modrih prog (število v km)
    smucisce['dolzina_rdecih'] = int(smucisce['dolzina_rdecih'])  # Dolžina rdečih prog (število v km)
    smucisce['dolzina_crnih'] = int(smucisce['dolzina_crnih'])  # Dolžina črnih prog (število v km)
    smucisce['stevilo_zicnic'] = int(smucisce['stevilo_zicnic'])  # Število žičnic (število)
    return smucisce

def prestej_ponovitve(vsebina):
    # Poiščem vsa ujemanja z uporabo findall
    ujemanja = vzorec_bloka.findall(vsebina) # Preštejem število ujemanj, mi jih da v seznam
    stevec = len(ujemanja)
    return stevec

with open('smucisca.html', 'r', encoding='utf-8') as f:
    stran = f.read()
    
# Preverim, ali imam prav
stevilo_blokov = prestej_ponovitve(stran)
print(f"Število smučišč: {stevilo_blokov}")






    
        
