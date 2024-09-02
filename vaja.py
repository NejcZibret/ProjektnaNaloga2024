import re
import html

def podatki_o_prebivalcih(niz):
    # Regularni izraz za iskanje vseh držav
    vzorec = r'<a[^>]*href="/world-population/[^"]+">([^<]+)</a>'
    
    # Poišče vsa ujemanja v nizu
    drzave = re.findall(vzorec, niz)
    
    # Dekodiranje HTML entitet in čiščenje odvečnih presledkov
    drzave = [html.unescape(re.sub(r'\s+', ' ', drzava).strip()) for drzava in drzave]
    
    return drzave  # Vrne seznam držav

# Branje vsebine HTML datoteke
with open('stran.html') as f:
    vsebina = f.read()

# Klic funkcije in izpis rezultatov
drzave = podatki_o_prebivalcih(vsebina)
for drzava in drzave:
    print(drzava)  # Izpis vseh najdenih držav


