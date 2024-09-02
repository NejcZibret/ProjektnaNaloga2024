import re

with open('stran.html') as f:
    vsebina = f.read()


def podatki_o_prebivalcih(niz):
    vzorec = (r'<a[^>]*href="/world-population/[^"]+">([^<]+)</a>')
    pojavitev = re.search(vzorec, niz)
    drzave = pojavitev.group('drzave')
    return drzave

drzave = podatki_o_prebivalcih(vsebina)
for drzava in drzave:
    print(drzava)  # Izpis vseh najdenih držav