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



