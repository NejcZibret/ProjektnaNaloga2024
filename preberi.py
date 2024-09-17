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








    
        
